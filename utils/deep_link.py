import base64
import hmac
import hashlib
import struct
from datetime import datetime

from utils.config import settings

SECRET_KEY = settings.SECRET_KEY.encode() if isinstance(settings.SECRET_KEY, str) else settings.SECRET_KEY


def base64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def base64url_decode(data: str) -> bytes:
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def encode_date_token(expire_date: datetime) -> str:
    timestamp = int(expire_date.timestamp())
    ts_bytes = struct.pack(">I", timestamp)
    signature = hmac.new(SECRET_KEY, ts_bytes, hashlib.sha256).digest()[:5]
    return f"{base64url(ts_bytes)}_{base64url(signature)}"


def decode_date_token(token: str) -> datetime | None:
    try:
        ts_b64, sig_b64 = token.split("_")
        ts_bytes = base64url_decode(ts_b64)
        signature = base64url_decode(sig_b64)
        expected_sig = hmac.new(SECRET_KEY, ts_bytes, hashlib.sha256).digest()[:5]
        if not hmac.compare_digest(signature, expected_sig):
            return None
        timestamp = struct.unpack(">I", ts_bytes)[0]
        return datetime.fromtimestamp(timestamp)
    except Exception:
        return None
