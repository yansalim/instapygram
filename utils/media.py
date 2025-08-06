"""
Media conversion utilities.

This module provides a helper to construct an in‑memory buffer from
either a base64 encoded string or a remote URL. It raises a
BadRequest when invalid data is provided or when the remote fetch
fails. The returned buffer is suitable for upload via instagrapi.
"""
import base64
import io

import requests
from werkzeug.exceptions import BadRequest


def get_buffer_from_source(data: dict) -> io.BytesIO:
    """Create a BytesIO buffer from a base64 or URL source.

    The input dict may include either a `base64` field (full data URI
    or just the base64 payload) or a `url` field. If neither is
    present, a BadRequest is raised.
    """
    # If base64 is provided, decode it
    if data.get("base64"):
        try:
            # In case a data URI prefix is included, split off the comma
            b64 = data["base64"].split(",", 1)[-1]
            decoded = base64.b64decode(b64)
            return io.BytesIO(decoded)
        except Exception as exc:
            raise BadRequest(f"base64 inválido: {exc}")
    # If a URL is provided, download it
    if url := data.get("url"):
        try:
            resp = requests.get(url, timeout=20)
            resp.raise_for_status()
            return io.BytesIO(resp.content)
        except Exception as exc:
            raise BadRequest(f"Erro ao baixar URL: {exc}")
    # Neither base64 nor url was provided
    raise BadRequest("Informe 'url' ou 'base64'")