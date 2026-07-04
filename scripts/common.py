"""Helpers dùng chung cho mọi crawler/validate/build script.

Chỉ dùng stdlib để môi trường nào cũng chạy được (không cần pip install).
Fetch đi qua proxy của môi trường (biến HTTPS_PROXY). Lỗi 403/blocked được
gói lại thành DomainBlocked để agent biết là thiếu domain trong allowlist,
KHÔNG phải lỗi parse.
"""
from __future__ import annotations

import csv
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

UA = "Mozilla/5.0 (vn-finance-dashboard; +https://github.com/quang-dobe/agents-vietname-finance-dashboard)"


class DomainBlocked(Exception):
    """Nguồn bị proxy chặn (403/407/405) — cần thêm domain vào allowlist."""


class FetchError(Exception):
    """Lỗi mạng/HTTP khác (timeout, 404, 5xx)."""


def fetch(url: str, retries: int = 2, delay: float = 1.5, timeout: int = 25) -> str:
    """GET một URL, trả về text. Retry với backoff cho lỗi mạng tạm thời.

    Raise DomainBlocked nếu bị proxy chặn (403/405/407) — đây là tín hiệu
    'thiếu allowlist', agent không được sửa script vì việc này.
    """
    last: Exception | None = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "vi,en;q=0.8"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                charset = resp.headers.get_content_charset() or "utf-8"
                return resp.read().decode(charset, errors="replace")
        except urllib.error.HTTPError as e:
            if e.code in (403, 405, 407):
                raise DomainBlocked(f"{url} -> HTTP {e.code} (proxy/allowlist)") from e
            last = e
        except urllib.error.URLError as e:
            # Proxy chặn domain ngoài allowlist trả 403/407 ở tầng CONNECT →
            # urllib báo "Tunnel connection failed: 403 Forbidden" (URLError, KHÔNG
            # phải HTTPError). Nhận diện để báo DomainBlocked, đừng nhầm là lỗi parse.
            reason = str(getattr(e, "reason", e))
            if re.search(r"[Tt]unnel connection failed:\s*(403|405|407)", reason):
                raise DomainBlocked(f"{url} -> {reason} (proxy/allowlist)") from e
            last = e
        except (TimeoutError, OSError) as e:
            last = e
        if attempt < retries:
            time.sleep(delay * (attempt + 1))
    raise FetchError(f"{url} -> {last}")


# ---------------------------------------------------------------------------
# Chuẩn hóa số kiểu Việt Nam
# ---------------------------------------------------------------------------
_NUM_RE = re.compile(r"-?\d[\d.,]*")


def vn_number(s: str) -> float:
    """'151.400.000' / '151,400' / '4,7%' / '26.460 ₫' -> float.

    Quy tắc: bỏ mọi ký tự không phải số/./,, sau đó suy luận dấu thập phân.
    - Nếu có cả '.' và ',': dấu xuất hiện SAU cùng là dấu thập phân (kiểu VN
      dùng '.' ngăn nghìn, ',' thập phân -> '1.234,5').
    - Nếu chỉ có một loại dấu và nó ngăn nhóm 3 chữ số -> dấu ngăn nghìn.
    """
    m = _NUM_RE.search(s.replace("\xa0", " "))
    if not m:
        raise ValueError(f"không tìm thấy số trong: {s!r}")
    tok = m.group(0)
    has_dot, has_com = "." in tok, "," in tok
    if has_dot and has_com:
        dec = "," if tok.rfind(",") > tok.rfind(".") else "."
        thou = "." if dec == "," else ","
        tok = tok.replace(thou, "").replace(dec, ".")
    elif has_com:
        tok = tok.replace(",", ".") if re.fullmatch(r"-?\d+,\d{1,2}", tok) else tok.replace(",", "")
    elif has_dot:
        tok = tok if re.fullmatch(r"-?\d+\.\d{1,2}", tok) else tok.replace(".", "")
    return float(tok)


def strip_tags(html: str) -> str:
    """Bỏ thẻ HTML, gộp khoảng trắng — dùng khi cần đọc text thô của 1 khối."""
    text = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;", " ", text)
    return re.sub(r"\s+", " ", text).strip()


# ---------------------------------------------------------------------------
# Ghi CSV append-only, 1 dòng / key (mặc định key = 'date')
# ---------------------------------------------------------------------------
def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def append_csv_row(path: Path, row: dict, fieldnames: list[str], key: str = "date") -> bool:
    """Thêm/ghi đè 1 dòng theo `key`, giữ file sort tăng dần theo key.

    Trả về True nếu file thay đổi nội dung.
    """
    rows = read_csv(path)
    by_key = {r[key]: r for r in rows}
    before = by_key.get(row[key])
    normalized = {k: ("" if row.get(k) is None else str(row.get(k, ""))) for k in fieldnames}
    if before == normalized:
        return False
    by_key[row[key]] = normalized
    out = [by_key[k] for k in sorted(by_key)]
    write_csv(path, fieldnames, out)
    return True


def load_json(path: Path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def emit(status: str, detail: str = "") -> None:
    """In dòng kết quả chuẩn mà agent đọc: OK / NO_CHANGE / NEW / FAIL."""
    print(f"{status} {detail}".rstrip())
