<div align="center">

# Genshin Replica Desk

**Packed via Axiox Media**

A local wizard that remaps every audio, texture, model and look value in alphardex/genshin-replica, then exports a playable HTML project zip.

<p>
  <a href="docs/README-zh.md"><img src="https://img.shields.io/badge/中文说明-README--zh-e7c07a?style=for-the-badge" alt="Chinese README" /></a>
</p>

<p>
  <a href="#install">Install</a> ·
  <a href="#features">Features</a> ·
  <a href="#requirements">Requirements</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="#documentation">FAQ</a>
</p>

<p>
  <img src="https://img.shields.io/badge/platform-Windows_10%2F11-0b0d12?style=flat-square" alt="Windows" />
  <img src="https://img.shields.io/badge/python-3.11%2B-e7c07a?style=flat-square" alt="Python" />
  <img src="https://img.shields.io/badge/ui-zh%20%2F%20en-7ee0c6?style=flat-square" alt="i18n" />
  <img src="https://img.shields.io/badge/export-HTML_zip-c9a227?style=flat-square" alt="export" />
</p>

</div>

<p align="center">
  <img src="docs/APPCap.png" width="100%" alt="Genshin Replica Desk preview">
</p>

> [!NOTE]
> The Windows EXE is unsigned. SmartScreen may warn on first launch.

---

## At a glance

| Item | Value |
|---|---|
| Product | Genshin Replica Desk |
| Vendor source | https://github.com/alphardex/genshin-replica |
| Output | Vite HTML project zip |
| UI | zh / en, gold default, light invert |

<a id="install"></a>

## Install

### 1. GitHub Deploy Desk (recommended)

One-click deploy this repository with [GitHub Deploy Desk](https://github.com/axioxmedia/github-deployer).

1. Get the deployer: https://github.com/axioxmedia/github-deployer
2. Paste this repo URL into Deploy Desk.
3. Read the README in the app, then confirm deploy.

That is the supported install path. Use the source / EXE steps below only if you are already building from a local checkout.

### 2. Run from source or freeze an EXE

```bat
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python app.py
```

Or double-click `build_exe.bat` and run `dist\GenshinReplicaDesk.exe`.

<a id="features"></a>

## Features

| Step | Action |
|---|---|
| Ready | Name the page and export folder. Vendor tree is already bundled. |
| Audio | Replace BGM and three door stingers. |
| Maps | Replace logo, enter bar, element ticker, cursor, skybox and login textures. |
| Models | Replace door / road / column / bridge / cloud GLBs. |
| Look | Fog, lights, sky gradient, camera FOV. |
| HUD | Optional glass strip: local time, region, weather. All off by default. |
| Export | HTML project zip. Book button removed. Untouched export keeps the original disclaimer. |

The circular book control (`ClickMe.png`) is treated as an invalid control and is never written into the zip. Click the scene to raise the door instead.

<a id="requirements"></a>

## Requirements

| | Minimum | Recommended |
|---|---|---|
| OS | Windows 10 | Windows 11 |
| Python | 3.11 | 3.12 |
| Exported project | Node 18 + npm | Node 20 |

<a id="architecture"></a>

## Architecture

```
FastAPI 127.0.0.1
  static wizard  +  vendor/genshin-replica
  uploads/       +  packer.py
pywebview window
PyInstaller onefile EXE
```

The exported zip is the original Vite + kokomi.js project with swapped files and patched TypeScript. Run `npm i` then `npm run dev` inside the unzipped folder.

<a id="documentation"></a>

## Documentation

<details>
<summary>Does an empty export keep the miHoYo disclaimer?</summary>

Yes. If no slot is replaced and no scene value / HUD flag / custom disclaimer is changed, the original bottom-left notice is copied verbatim.
</details>

<details>
<summary>Where do I drop a screenshot for GitHub?</summary>

Save a window capture as `docs/APPCap.png` (this README already points there).
</details>

Packed via Axiox Media · [axiox.media](https://axiox.media)
