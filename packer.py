"""Emit a static HTML folder that a normal web server can host."""

from __future__ import annotations

import json
import shutil
import zipfile
from pathlib import Path
from typing import Any

from catalog import ALL_SLOTS, DEFAULT_SCENE, ORIGINAL_DISCLAIMER, REMOVED_SLOT

HUD_JS = r"""
(function () {
  var flags = window.__REPLICA_HUD__ || {};
  if (!flags.time && !flags.region && !flags.weather) return;
  var box = document.createElement("aside");
  box.className = "local-glass-hud";
  box.innerHTML =
    (flags.time ? '<div class="hud-row"><span class="hud-k">TIME</span><span data-hud="time">--:--:--</span></div>' : "") +
    (flags.region ? '<div class="hud-row"><span class="hud-k">REGION</span><span data-hud="region"></span></div>' : "") +
    (flags.weather ? '<div class="hud-row"><span class="hud-k">WEATHER</span><span data-hud="weather">…</span></div>' : "");
  document.body.appendChild(box);
  var timeEl = box.querySelector('[data-hud="time"]');
  var regionEl = box.querySelector('[data-hud="region"]');
  var weatherEl = box.querySelector('[data-hud="weather"]');
  if (regionEl) {
    var tz = (Intl.DateTimeFormat().resolvedOptions().timeZone || "Local");
    regionEl.textContent = navigator.language ? tz + " · " + navigator.language : tz;
  }
  if (timeEl) {
    var tick = function () {
      timeEl.textContent = new Date().toLocaleTimeString(undefined, { hour12: false });
    };
    tick();
    setInterval(tick, 1000);
  }
  if (weatherEl) {
    var apply = function (lat, lon) {
      fetch("https://api.open-meteo.com/v1/forecast?latitude=" + lat + "&longitude=" + lon + "&current=temperature_2m,weather_code")
        .then(function (r) { return r.json(); })
        .then(function (data) {
          var cur = data.current || {};
          weatherEl.textContent = (cur.weather_code != null ? "WMO " + cur.weather_code : "Weather") + "  " + cur.temperature_2m + ((data.current_units && data.current_units.temperature_2m) || "°C");
        })
        .catch(function () { weatherEl.textContent = "—"; });
    };
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        function (pos) { apply(pos.coords.latitude, pos.coords.longitude); },
        function () { apply(22.3, 114.2); },
        { timeout: 4000 }
      );
    } else apply(22.3, 114.2);
  }
})();
"""

HUD_CSS = """
.local-glass-hud{position:fixed;z-index:20;top:18px;left:18px;min-width:220px;padding:12px 16px;border-radius:16px;color:#f4f7fb;font-family:"Segoe UI","Noto Sans SC",sans-serif;font-size:13px;letter-spacing:.04em;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.28);box-shadow:0 12px 40px rgba(8,20,40,.18);backdrop-filter:blur(18px) saturate(1.35);-webkit-backdrop-filter:blur(18px) saturate(1.35);pointer-events:none;user-select:none}
.local-glass-hud .hud-row{display:flex;justify-content:space-between;gap:16px;line-height:1.7}
.local-glass-hud .hud-k{opacity:.62;font-size:10px;letter-spacing:.16em}
"""


def _safe_rel(rel: str) -> Path:
    p = Path(rel.replace("\\", "/"))
    if p.is_absolute() or ".." in p.parts:
        raise ValueError(f"unsafe path {rel}")
    return p


def project_is_pristine(project: dict[str, Any], replaced: list[str]) -> bool:
    if replaced:
        return False
    scene = project.get("scene") or {}
    for key, val in DEFAULT_SCENE.items():
        if scene.get(key, val) != val:
            return False
    if (project.get("title") or DEFAULT_SCENE["pageTitle"]) != DEFAULT_SCENE["pageTitle"]:
        return False
    if project.get("hudTime") or project.get("hudRegion") or project.get("hudWeather"):
        return False
    mode = project.get("disclaimerMode") or "original"
    text = (project.get("disclaimerText") or "").strip()
    if mode != "original" and text and text != ORIGINAL_DISCLAIMER.strip():
        return False
    return True


def _is_static_site(folder: Path) -> bool:
    return (folder / "index.html").exists() and any((folder / "assets").glob("*.js"))


def ensure_static_runtime(vendor: Path, extra_roots: list[Path] | None = None) -> Path:
    """Locate the prebuilt static site. Never require Node at export time."""
    here = Path(__file__).resolve().parent
    roots = [here]
    if extra_roots:
        roots.extend(extra_roots)
    candidates: list[Path] = []
    for root in roots:
        candidates.extend(
            [
                root / "static" / "export-template",
                root / "runtime" / "static-site",
                root / "vendor" / "genshin-replica" / "dist",
            ]
        )
    candidates.extend(
        [
            vendor / "dist",
            vendor.parent.parent / "static" / "export-template",
            vendor.parent.parent / "runtime" / "static-site",
        ]
    )
    seen: set[Path] = set()
    for dest in candidates:
        try:
            dest = dest.resolve()
        except OSError:
            continue
        if dest in seen:
            continue
        seen.add(dest)
        if _is_static_site(dest):
            return dest
    raise RuntimeError(
        "缺少预编译页面（static/export-template）。请关闭旧的 exe，用当前目录的 start.bat / app.py 启动。"
    )


GSTATIC_DRACO = "https://www.gstatic.com/draco/versioned/decoders/1.5.7/"
LOCAL_DRACO = "./draco/"


def _localize_bundle(work: Path) -> None:
    here = Path(__file__).resolve().parent
    srcs = [
        work / "draco",
        here / "static" / "export-template" / "draco",
        here / "static" / "vendor" / "three" / "examples" / "jsm" / "libs" / "draco" / "gltf",
    ]
    dest = work / "draco"
    dest.mkdir(parents=True, exist_ok=True)
    for src in srcs:
        if not src.exists():
            continue
        for item in src.iterdir():
            if item.is_file():
                target = dest / item.name
                if not target.exists():
                    shutil.copy2(item, target)
    for glb in work.rglob("*.glb"):
        alias = glb.with_suffix(".mp3")
        if not alias.exists():
            shutil.copy2(glb, alias)
    assets = work / "assets"
    if assets.exists():
        for js in assets.glob("*.js"):
            text = js.read_text(encoding="utf-8", errors="replace")
            text = text.replace(GSTATIC_DRACO, LOCAL_DRACO)
            text = text.replace('decoderConfig.type==="js"', "true")
            text = text.replace(".glb", ".mp3")
            js.write_text(text, encoding="utf-8")


def _inject_index(index: Path, title: str, config: dict[str, Any], hud: dict[str, bool]) -> None:
    html = index.read_text(encoding="utf-8")
    html = html.replace("<title>原神启动</title>", f"<title>{title}</title>")
    html = html.replace("<title>Vite App</title>", f"<title>{title}</title>")
    html = html.replace(" crossorigin", "")
    boot = (
        "<script>window.__REPLICA_CONFIG__="
        + json.dumps(config, ensure_ascii=False)
        + ";window.__REPLICA_HUD__="
        + json.dumps(hud)
        + ";</script>\n"
        "<style>" + HUD_CSS + "</style>\n"
        "<script>" + HUD_JS + "</script>\n"
        "<script>if(location.protocol==='file:'){document.addEventListener('DOMContentLoaded',function(){var n=document.createElement('div');n.style.cssText='position:fixed;inset:0;z-index:99;background:#111;color:#f3e2b8;padding:32px;font:16px/1.6 sans-serif';n.textContent='不要用 file:// 打开。请把整个文件夹上传到静态服务器，或在本目录执行 python -m http.server 8080';document.body.appendChild(n);});}</script>\n"
    )
    marker = '<script type="module"'
    if marker in html:
        html = html.replace(marker, boot + marker, 1)
    elif "</head>" in html:
        html = html.replace("</head>", boot + "</head>", 1)
    else:
        html = boot + html
    index.write_text(html, encoding="utf-8")


def build_export(
    vendor: Path,
    uploads: Path,
    work: Path,
    zip_path: Path,
    project: dict[str, Any],
    replaced_ids: list[str],
    extra_roots: list[Path] | None = None,
) -> dict[str, Any]:
    runtime = ensure_static_runtime(vendor, extra_roots=extra_roots)
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True, exist_ok=True)
    for item in runtime.iterdir():
        dest = work / item.name
        if item.is_dir() and item.name in {"Genshin", "textures"}:
            continue
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)
    public = vendor / "public"
    if public.exists():
        for item in public.iterdir():
            dest = work / item.name
            if item.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)

    applied: list[str] = []
    for slot_id in replaced_ids:
        meta = ALL_SLOTS.get(slot_id)
        if not meta:
            continue
        src = uploads / slot_id
        if not src.exists() or not src.is_file():
            matches = list(uploads.glob(f"{slot_id}.*"))
            src = matches[0] if matches else src
        if not src.exists():
            continue
        # Vite copies public/ to dist root, dropping the public/ prefix.
        rel = _safe_rel(meta["path"])
        dest_rel = Path(*rel.parts[1:]) if rel.parts and rel.parts[0] == "public" else rel
        dest = work / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        applied.append(slot_id)

    click = work / "Genshin" / "ClickMe.png"
    click.unlink(missing_ok=True)

    scene = {**DEFAULT_SCENE, **(project.get("scene") or {})}
    title = (project.get("title") or scene.get("pageTitle") or "原神启动").strip()
    pristine = project_is_pristine(project, applied)
    cfg: dict[str, Any] = {
        "fogColor": scene.get("fogColor"),
        "fogNear": scene.get("fogNear"),
        "fogFar": scene.get("fogFar"),
        "ambientColor": scene.get("ambientColor"),
        "ambientIntensity": scene.get("ambientIntensity"),
        "dirColor": scene.get("dirColor"),
        "dirIntensity": scene.get("dirIntensity"),
        "bgColor1": scene.get("bgColor1"),
        "bgColor2": scene.get("bgColor2"),
        "bgColor3": scene.get("bgColor3"),
        "bgStop1": scene.get("bgStop1"),
        "bgStop2": scene.get("bgStop2"),
        "cameraFov": scene.get("cameraFov"),
        "cameraTilt": scene.get("cameraTilt"),
    }
    if not pristine and (project.get("disclaimerMode") or "original") != "original":
        cfg["disclaimer"] = project.get("disclaimerText") or ORIGINAL_DISCLAIMER
    hud = {
        "time": bool(project.get("hudTime")),
        "region": bool(project.get("hudRegion")),
        "weather": bool(project.get("hudWeather")),
    }
    _localize_bundle(work)
    _inject_index(work / "index.html", title, cfg, hud)
    (work / "replica.desk.json").write_text(
        json.dumps(
            {
                "generator": "Genshin Replica Desk",
                "kind": "static-html",
                "pristine": pristine,
                "appliedSlots": applied,
                "removedDoorClick": True,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (work / "README.txt").write_text(
        "Static site. Upload this whole folder to any static host "
        "(Nginx / GitHub Pages / Vercel static / OSS).\n"
        "Open the hosted URL. Do not open index.html as a file:// page.\n"
        "The door-click / enter-game event is disabled.\n",
        encoding="utf-8",
    )

    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in work.rglob("*"):
            if file.is_file():
                zf.write(file, file.relative_to(work.parent))
    return {
        "path": str(zip_path),
        "size": zip_path.stat().st_size,
        "pristine": pristine,
        "applied": applied,
        "folder": work.name,
    }
