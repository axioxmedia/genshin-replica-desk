"""Axiox Media packer watermark and window-title helpers."""

from __future__ import annotations

import locale
import os
import sys
from pathlib import Path

AIO_BRAND = "Axiox Media"
AXIOXMEDIA_MARK = "axioxmedia"
AXIOX_PACKER_ZH = "由安溯媒体自动打包，软件名："
AXIOX_PACKER_EN = "Packed via Axiox Media, software name: "
AIO_SOFTWARE_NAME_ZH = "原神复刻编辑台"
AIO_SOFTWARE_NAME_EN = "Genshin Replica Desk"


def axiox_os_is_chinese() -> bool:
    if os.name == "nt":
        try:
            import ctypes

            lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            if (lang_id & 0xFF) == 0x04:
                return True
        except Exception:
            pass
    candidates = [
        os.environ.get("LANG", ""),
        os.environ.get("LANGUAGE", ""),
        locale.getlocale()[0] or "",
    ]
    try:
        candidates.append(locale.getdefaultlocale()[0] or "")
    except Exception:
        pass
    blob = " ".join(candidates).lower()
    return "zh" in blob or "chinese" in blob


def axiox_window_title() -> str:
    if axiox_os_is_chinese():
        return f"{AXIOX_PACKER_ZH}{AIO_SOFTWARE_NAME_ZH}"
    return f"{AXIOX_PACKER_EN}{AIO_SOFTWARE_NAME_EN}"


def aio_watermark() -> dict[str, str]:
    return {
        "brand": AIO_BRAND,
        "mark": AXIOXMEDIA_MARK,
        "software_zh": AIO_SOFTWARE_NAME_ZH,
        "software_en": AIO_SOFTWARE_NAME_EN,
        "title": axiox_window_title(),
    }


def aio_logo_png() -> bytes:
    from aio_logo import aio_logo_png as _png

    return _png()
