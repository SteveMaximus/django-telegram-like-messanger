
import base64
from django.conf import settings


def _xor_bytes(data: bytes, key: bytes) -> bytes:
    """XOR two byte sequences, cycling the key if necessary.

    Working with raw bytes avoids Unicode issues and allows encrypting
    arbitrary data (attachments later?).
    """
    from itertools import cycle
    return bytes(a ^ b for a, b in zip(data, cycle(key)))


def encrypt(text: str, key: str | None = None) -> str:
    """Return a base64‑encoded XOR cipher of ``text``.

    ``key`` defaults to :data:`django.conf.settings.SECRET_KEY`.
    The output can be stored in the database safely and fed to
    :func:`decrypt` when reading.
    """
    if key is None:
        key = settings.SECRET_KEY
    raw = text.encode("utf-8")
    encrypted = _xor_bytes(raw, key.encode("utf-8"))
    return base64.b64encode(encrypted).decode("ascii")


def decrypt(encoded: str, key: str | None = None) -> str:
    """Decode data produced by :func:`encrypt`.

    Returns an empty string on failure so callers can display a placeholder.
    """
    if not encoded:
        return ""
    if key is None:
        key = settings.SECRET_KEY
    try:
        encrypted = base64.b64decode(encoded)
        decrypted = _xor_bytes(encrypted, key.encode("utf-8"))
        return decrypted.decode("utf-8")
    except Exception:
        return ""