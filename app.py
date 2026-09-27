"""Genshin Replica Desk — local wizard that remaps alphardex/genshin-replica and exports HTML."""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from aio_logo import aio_logo_png, apply_hwnd_icon, write_build_icon  # noqa: F401
from axioxmedia import (
    AIO_BRAND,
    AIO_SOFTWARE_NAME_EN,
    aio_watermark,
    axiox_window_title,
)
from catalog import ALL_SLOTS, DEFAULT_PROJECT, catalog_payload
from packer import build_export
from utm_beacon import schedule_utm_beacon

APP_VERSION = "1.3.4"


def app_root() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


def runtime_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


ROOT = app_root()
STATIC = ROOT / "static"
VENDOR = ROOT / "vendor" / "genshin-replica"
RUNTIME = runtime_dir()
DATA = RUNTIME / "data"
UPLOADS = DATA / "uploads"
EXPORTS = DATA / "exports"
PREFS_FILE = RUNTIME / "genshin-replica-desk-prefs.json"
PROJECT_FILE = DATA / "project.json"
ZIP_NAME = "genshin-replica-html.zip"

DATA.mkdir(parents=True, exist_ok=True)
UPLOADS.mkdir(parents=True, exist_ok=True)
EXPORTS.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Genshin Replica Desk", version=APP_VERSION)
app.mount("/assets", StaticFiles(directory=STATIC), name="assets")


@app.exception_handler(Exception)
async def json_errors(_request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, HTTPException):
        return JSONResponse({"ok": False, "detail": exc.detail}, status_code=exc.status_code)
    return JSONResponse({"ok": False, "detail": str(exc) or exc.__class__.__name__}, status_code=500)


class ProjectBody(BaseModel):
    title: str = "原神启动"
    folderName: str = "genshin-replica-export"
    exportDir: str = ""
    scene: dict[str, Any] = Field(default_factory=dict)
    hudTime: bool = False
    hudRegion: bool = False
    hudWeather: bool = False
    disclaimerMode: str = "original"
    disclaimerText: str = ""
    remember: bool = True


class ExportBody(BaseModel):
    destDir: str = ""
    folderName: str = ""


class PathBody(BaseModel):
    path: str = ""


class PrefsBody(BaseModel):
    prefs: dict[str, Any]


def load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return fallback


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def current_project() -> dict[str, Any]:
    stored = load_json(PROJECT_FILE, {})
    merged = json.loads(json.dumps(DEFAULT_PROJECT))
    if isinstance(stored, dict):
        merged.update({k: v for k, v in stored.items() if k != "scene"})
        if isinstance(stored.get("scene"), dict):
            merged["scene"].update(stored["scene"])
    return merged


def list_replaced() -> list[str]:
    found: list[str] = []
    for slot_id in ALL_SLOTS:
        if resolve_upload(slot_id) is not None:
            found.append(slot_id)
    return found


def resolve_upload(slot_id: str) -> Path | None:
    direct = UPLOADS / slot_id
    if direct.exists() and direct.is_file():
        return direct
    matches = sorted(UPLOADS.glob(f"{slot_id}.*"))
    return matches[0] if matches else None


def resolve_slot_file(slot_id: str) -> Path:
    uploaded = resolve_upload(slot_id)
    if uploaded is not None:
        return uploaded
    meta = ALL_SLOTS.get(slot_id)
    if not meta:
        raise HTTPException(404, f"unknown slot {slot_id}")
    vendor_file = VENDOR / meta["path"]
    if not vendor_file.exists():
        raise HTTPException(404, f"missing vendor file for {slot_id}")
    return vendor_file


def guess_mime(path: Path) -> str:
    ext = path.suffix.lower()
    return {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
        ".ogg": "audio/ogg",
        ".glb": "model/gltf-binary",
        ".gltf": "model/gltf+json",
    }.get(ext, "application/octet-stream")


def default_export_root() -> str:
    if os.name == "nt":
        d = Path("D:/")
        if d.exists():
            return str(Path("D:/Projects"))
        return str(Path.home() / "Projects")
    for candidate in ("/mnt/d/Projects", "/media/d/Projects"):
        if Path(candidate).parent.exists():
            return candidate
    return str(Path.home() / "Projects")


def safe_dest_dir(raw: str) -> Path:
    text = (raw or "").strip()
    if not text:
        raise HTTPException(400, "请选择导出目录")
    dest = Path(text).expanduser()
    if not dest.is_absolute():
        raise HTTPException(400, "导出路径必须是绝对路径")
    dest.mkdir(parents=True, exist_ok=True)
    return dest


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


@app.get("/brand/logo.png")
def brand_logo() -> Response:
    return Response(content=aio_logo_png(), media_type="image/png")


@app.get("/favicon.ico")
def brand_favicon() -> Response:
    return Response(content=aio_logo_png(), media_type="image/png")


@app.get("/api/defaults")
def api_defaults() -> dict[str, Any]:
    return {
        "version": APP_VERSION,
        "platform": sys.platform,
        "is_windows": os.name == "nt",
        "aio_brand": AIO_BRAND,
        "axiox_title": axiox_window_title(),
        "axioxmedia": aio_watermark(),
        "vendorReady": VENDOR.exists() and (VENDOR / "package.json").exists(),
        "replaced": list_replaced(),
        "exportDir": default_export_root(),
        "prefer_d": os.name == "nt" and Path("D:/").exists(),
    }


@app.get("/api/catalog")
def api_catalog() -> dict[str, Any]:
    payload = catalog_payload()
    payload["replaced"] = list_replaced()
    return payload


@app.get("/api/prefs")
def api_get_prefs() -> dict[str, Any]:
    return {"prefs": load_json(PREFS_FILE, {})}


@app.post("/api/prefs")
def api_set_prefs(body: PrefsBody) -> dict[str, Any]:
    save_json(PREFS_FILE, body.prefs)
    return {"ok": True}


@app.get("/api/project")
def api_get_project() -> dict[str, Any]:
    return {"project": current_project(), "replaced": list_replaced()}


@app.put("/api/project")
def api_put_project(body: ProjectBody) -> dict[str, Any]:
    payload = body.model_dump()
    save_json(PROJECT_FILE, payload)
    return {"ok": True, "project": current_project()}


@app.post("/api/upload/{slot_id}")
async def api_upload(slot_id: str, file: UploadFile = File(...)) -> dict[str, Any]:
    if slot_id not in ALL_SLOTS:
        raise HTTPException(400, f"unknown slot {slot_id}")
    dest = UPLOADS / slot_id
    raw = await file.read()
    if not raw:
        raise HTTPException(400, "empty file")
    dest.write_bytes(raw)
    return {"ok": True, "slot": slot_id, "size": len(raw), "replaced": list_replaced()}


@app.get("/api/asset/{slot_id}")
def api_asset(slot_id: str) -> FileResponse:
    if slot_id not in ALL_SLOTS:
        raise HTTPException(400, f"unknown slot {slot_id}")
    path = resolve_slot_file(slot_id)
    return FileResponse(
        path,
        media_type=guess_mime(path),
        filename=path.name,
        headers={"Cache-Control": "no-store"},
    )


@app.post("/api/pick-folder")
def api_pick_folder() -> dict[str, Any]:
    chosen = ""
    try:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        chosen = filedialog.askdirectory(title="Export folder") or ""
        root.destroy()
    except Exception as exc:
        write_log(f"folder picker skipped: {exc}")
        chosen = ""
    return {"path": chosen, "fallback": default_export_root()}


@app.post("/api/validate-dir")
def api_validate_dir(body: PathBody) -> dict[str, Any]:
    dest = safe_dest_dir(body.path)
    return {"ok": True, "path": str(dest), "exists": dest.exists()}


@app.delete("/api/upload/{slot_id}")
def api_clear_slot(slot_id: str) -> dict[str, Any]:
    if slot_id not in ALL_SLOTS:
        raise HTTPException(400, f"unknown slot {slot_id}")
    target = UPLOADS / slot_id
    target.unlink(missing_ok=True)
    for extra in UPLOADS.glob(f"{slot_id}.*"):
        extra.unlink(missing_ok=True)
    return {"ok": True, "replaced": list_replaced()}


@app.post("/api/export")
def api_export(body: ExportBody | None = None) -> dict[str, Any]:
    if not VENDOR.exists():
        return JSONResponse({"ok": False, "detail": "vendor replica is missing"}, status_code=500)
    project = current_project()
    payload = body.model_dump() if body else {}
    folder = (payload.get("folderName") or project.get("folderName") or "genshin-replica-export").strip()
    dest_raw = (payload.get("destDir") or project.get("exportDir") or "").strip()
    zip_name = f"{folder}.zip" if folder else ZIP_NAME
    zip_path = EXPORTS / zip_name
    work = Path(tempfile.mkdtemp(prefix="grd-export-")) / folder
    try:
        info = build_export(
            vendor=VENDOR,
            uploads=UPLOADS,
            work=work,
            zip_path=zip_path,
            project=project,
            replaced_ids=list_replaced(),
            extra_roots=[ROOT, RUNTIME],
        )
    except Exception as exc:
        return JSONResponse({"ok": False, "detail": f"打包失败: {exc}"}, status_code=500)
    finally:
        shutil.rmtree(work.parent, ignore_errors=True)
    saved = ""
    if dest_raw:
        try:
            dest = safe_dest_dir(dest_raw)
            target = dest / zip_name
            shutil.copy2(zip_path, target)
            saved = str(target)
            project["exportDir"] = str(dest)
            project["folderName"] = folder
            save_json(PROJECT_FILE, project)
        except HTTPException as exc:
            saved = ""
            info["copyWarning"] = str(exc.detail)
        except Exception as exc:
            saved = ""
            info["copyWarning"] = str(exc)
    return {
        "ok": True,
        "filename": zip_name,
        "size": info["size"],
        "pristine": info["pristine"],
        "applied": info["applied"],
        "saved": saved,
        "warning": info.get("copyWarning") or "",
        "download": "/api/export/download?name=" + zip_name,
    }


@app.get("/api/export/download")
def api_download(name: str = "") -> FileResponse:
    filename = Path(name or ZIP_NAME).name
    zip_path = EXPORTS / filename
    if not zip_path.exists():
        fallback = EXPORTS / ZIP_NAME
        if fallback.exists():
            zip_path = fallback
            filename = ZIP_NAME
        else:
            raise HTTPException(404, "export the project first")
    return FileResponse(zip_path, filename=filename, media_type="application/zip")


LOG_FILE = runtime_dir() / "genshin_replica_desk.log"


def write_log(message: str) -> None:
    try:
        with LOG_FILE.open("a", encoding="utf-8") as fh:
            fh.write(message.rstrip() + "\n")
    except OSError:
        pass


def show_error(message: str) -> None:
    write_log(message)
    if os.name == "nt":
        try:
            import ctypes

            ctypes.windll.user32.MessageBoxW(0, message, "Genshin Replica Desk", 0x10)
            return
        except Exception:
            pass
    print(message, file=sys.stderr)


def _free_port(preferred: int = 8787) -> int:
    import socket

    for port in (preferred, 8788, 8789, 8790, 0):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("127.0.0.1", port))
            chosen = int(sock.getsockname()[1])
        except OSError:
            chosen = -1
        finally:
            sock.close()
        if chosen > 0:
            return chosen
    raise RuntimeError("没有可用的本地端口")


def ensure_stdio() -> None:
    if sys.stdout is None:
        sys.stdout = LOG_FILE.open("a", encoding="utf-8")
    if sys.stderr is None:
        sys.stderr = LOG_FILE.open("a", encoding="utf-8")


def run_server(host: str, port: int, reload: bool = False) -> None:
    import uvicorn

    ensure_stdio()
    if reload:
        uvicorn.run(app, host=host, port=port, reload=True, log_level="warning", log_config=None)
        return
    config = uvicorn.Config(
        app,
        host=host,
        port=port,
        log_level="warning",
        log_config=None,
        lifespan="on",
        access_log=False,
    )
    server = uvicorn.Server(config)
    server.install_signal_handlers = False
    server.run()


def wait_ready(url: str, server_error: list[str], timeout: float = 30.0) -> None:
    import time

    deadline = time.time() + timeout
    while time.time() < deadline:
        if server_error:
            raise RuntimeError(server_error[0])
        try:
            with httpx.Client(timeout=0.8, trust_env=False) as http:
                if http.get(url).status_code < 500:
                    return
        except httpx.HTTPError:
            time.sleep(0.2)
    extra = f"\n服务线程错误：{server_error[0]}" if server_error else ""
    raise RuntimeError(f"本地服务启动超时：{url}{extra}\n日志：{LOG_FILE}")


def run_desktop() -> None:
    import threading
    import traceback
    import webbrowser

    write_log(f"start frozen={getattr(sys, 'frozen', False)} meipass={getattr(sys, '_MEIPASS', '')}")
    write_log(f"static={STATIC} exists={STATIC.exists()} vendor={VENDOR.exists()}")

    port = _free_port()
    url = f"http://127.0.0.1:{port}"
    write_log(f"bind {url}")
    server_error: list[str] = []

    def _serve() -> None:
        try:
            run_server("127.0.0.1", port, reload=False)
        except Exception:
            server_error.append(traceback.format_exc())
            write_log(server_error[-1])

    thread = threading.Thread(target=_serve, name="uvicorn", daemon=True)
    thread.start()
    wait_ready(f"{url}/api/defaults", server_error)
    schedule_utm_beacon(product_en=AIO_SOFTWARE_NAME_EN, version=app.version, log=write_log)

    try:
        import webview

        window = webview.create_window(
            title=axiox_window_title(),
            url=url,
            width=1440,
            height=900,
            min_size=(960, 680),
            background_color="#0b0d12",
        )

        def paint_chrome(_=None) -> None:
            if os.name != "nt":
                return
            try:
                import ctypes

                hwnd = int(window.native.Handle.ToInt32())
                apply_hwnd_icon(hwnd)
                value = ctypes.c_int(1)
                for attr in (20, 19):
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        hwnd, attr, ctypes.byref(value), ctypes.sizeof(value)
                    )
            except Exception as exc:
                write_log(f"dark titlebar skipped: {exc}")

        try:
            window.events.shown += paint_chrome
        except Exception:
            pass
        webview.start()
        return
    except Exception:
        write_log(traceback.format_exc())
        webbrowser.open(url)
        while thread.is_alive():
            thread.join(timeout=0.5)


if __name__ == "__main__":
    import multiprocessing
    import traceback

    multiprocessing.freeze_support()
    ensure_stdio()
    try:
        desktop = "--web" not in sys.argv and os.environ.get("DEPLOY_DESK_WEB") != "1"
        if desktop:
            run_desktop()
        else:
            run_server("127.0.0.1", _free_port(8787), reload=not getattr(sys, "frozen", False))
    except Exception:
        show_error("启动失败：\n\n" + traceback.format_exc() + f"\n\n日志文件：{LOG_FILE}")
        raise
