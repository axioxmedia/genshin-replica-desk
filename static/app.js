const SLUG = "genshin-replica-desk";
const LAST = 6;
const PREF_KEY = SLUG + ".prefs";
const I18N = {
  zh: {
    appTitle: "原神复刻编辑台",
    appSubtitle: "替换音乐、交互、模型与材质，导出可运行的 HTML 工程包",
    themeGold: "黑金",
    themeLight: "浅色",
    s0Title: "准备工程",
    s0Lead: "已内置 alphardex/genshin-replica。命名本次衍生，然后按步骤替换资源。",
    s0Notice: "右侧书本按钮（ClickMe.png）会被永久移除：原项目里该控件无有效功能。未改任何资源直接导出时，将原样保留左下角 miHoYo 免责声明。",
    titleLabel: "页面标题",
    folderLabel: "导出文件夹名",
    remember: "记住本次选择",
    next: "下一步",
    back: "上一步",
    s1Title: "音乐与音效",
    s1Lead: "替换 BGM 与三道过场音效。留空则使用原项目音频。",
    s2Title: "界面与材质贴图",
    s2Lead: "Logo、进入条、元素进度、指针、天空盒与登录场景贴图。",
    s3Title: "模型",
    s3Lead: "上传 GLB / glTF 以替换门、路、柱、桥、云与光柱。",
    s4Title: "光照与材质参数",
    s4Lead: "雾、环境光、主光与天空渐变。数值保持原值即视为未编辑。",
    s5Title: "本地状态玻璃条",
    s5Lead: "可选：在导出页左上角显示毛玻璃信息。三项默认关闭。",
    hudTime: "系统时间",
    hudTimeHint: "本机当前时钟，每秒刷新",
    hudRegion: "地区",
    hudRegionHint: "时区与浏览器语言区域",
    hudWeather: "天气",
    hudWeatherHint: "Open-Meteo 当前天气（需联网，可请求定位）",
    s6Title: "声明并导出 HTML",
    s6Lead: "未编辑任何内容时强制保留原免责声明。若改写了资源，可选择自定义声明文本。",
    discMode: "免责声明",
    discOriginal: "保留原项目左下角声明（推荐，未编辑时强制）",
    discCustom: "使用下面的自定义文本",
    export: "导出静态站点 Zip",
    replace: "替换",
    clear: "还原",
    replaced: "已替换",
    stock: "原资源",
    steps: ["准备", "音频", "贴图", "模型", "材质", "玻璃条", "导出"],
    exported: "已生成可上传的静态站点 zip。",
    exportFail: "导出失败",
    vendorOk: "vendor 已就绪",
    vendorMissing: "未找到内置 replica",
    preview: "试听",
    stop: "停止",
    view3d: "3D 预览",
    livePreview: "实时预览",
    close: "关闭",
    cancel: "取消",
    browse: "浏览",
    exportWhere: "选择导出位置",
    exportWhereLead: "选择本机目录。确认后会在该目录写入 zip，并同时提供浏览器下载。",
    exportDirLabel: "导出目录",
    exportConfirm: "确认导出",
    pickFail: "无法打开系统目录框，请手动填写路径。",
    savedTo: "已写入",
  },
  en: {
    appTitle: "Genshin Replica Desk",
    appSubtitle: "Replace music, interaction, models and materials, then export an HTML project zip",
    themeGold: "Gold",
    themeLight: "Light",
    s0Title: "Prepare the project",
    s0Lead: "alphardex/genshin-replica is bundled. Name this derivative, then replace assets step by step.",
    s0Notice: "The book button (ClickMe.png) is always stripped: it has no valid function. An untouched export keeps the original bottom-left miHoYo disclaimer.",
    titleLabel: "Page title",
    folderLabel: "Export folder name",
    remember: "Remember these choices",
    next: "Next",
    back: "Back",
    s1Title: "Music and cues",
    s1Lead: "Replace the BGM and three stingers. Leave a slot empty to keep the vendor file.",
    s2Title: "UI and material maps",
    s2Lead: "Logo, enter bar, element ticker, cursor, skybox and login textures.",
    s3Title: "Models",
    s3Lead: "Upload GLB / glTF for the door, road, columns, bridges, clouds and light mesh.",
    s4Title: "Light and material values",
    s4Lead: "Fog, ambient, key light and sky gradient. Unchanged numbers count as not edited.",
    s5Title: "Local glass HUD",
    s5Lead: "Optional frosted strip at the top-left of the exported page. All three boxes start unchecked.",
    hudTime: "System time",
    hudTimeHint: "Local clock, refreshed every second",
    hudRegion: "Region",
    hudRegionHint: "Time zone and browser locale",
    hudWeather: "Weather",
    hudWeatherHint: "Open-Meteo current conditions (needs network, may request geolocation)",
    s6Title: "Disclaimer and HTML export",
    s6Lead: "An untouched project always keeps the original disclaimer. Custom text is available only after edits.",
    discMode: "Disclaimer",
    discOriginal: "Keep the original bottom-left notice (forced when nothing was edited)",
    discCustom: "Use the custom text below",
    export: "Export static site zip",
    replace: "Replace",
    clear: "Revert",
    replaced: "Replaced",
    stock: "Vendor",
    steps: ["Ready", "Audio", "Maps", "Models", "Look", "HUD", "Export"],
    exported: "Static site zip ready.",
    exportFail: "Export failed",
    vendorOk: "Vendor replica ready",
    vendorMissing: "Bundled replica missing",
    preview: "Preview",
    stop: "Stop",
    view3d: "3D preview",
    livePreview: "Live preview",
    close: "Close",
    cancel: "Cancel",
    browse: "Browse",
    exportWhere: "Choose export folder",
    exportWhereLead: "Pick a local folder. The zip is written there and also offered as a download.",
    exportDirLabel: "Export directory",
    exportConfirm: "Export now",
    pickFail: "The system folder dialog was unavailable. Type a path instead.",
    savedTo: "Saved to",
  },
};

const SCENE_FIELDS = [
  ["fogColor", "Fog", "color"],
  ["fogNear", "Fog near", "number"],
  ["fogFar", "Fog far", "number"],
  ["ambientColor", "Ambient", "color"],
  ["ambientIntensity", "Ambient I", "number"],
  ["dirColor", "Key light", "color"],
  ["dirIntensity", "Key I", "number"],
  ["bgColor1", "Sky 1", "color"],
  ["bgColor2", "Sky 2", "color"],
  ["bgColor3", "Sky 3", "color"],
  ["bgStop1", "Stop 1", "number"],
  ["bgStop2", "Stop 2", "number"],
  ["cameraFov", "FOV", "number"],
  ["cameraTilt", "Tilt °", "number"],
];

let currentStep = 0;
let catalog = { audio: [], images: [], models: [], defaults: { scene: {} } };
let replaced = new Set();
let uiLang = "zh";
let playing = null;
let lookRaf = 0;

function detectUiLang() {
  const saved = localStorage.getItem("aio.uiLang");
  if (saved === "zh" || saved === "en") return saved;
  return (navigator.language || "").toLowerCase().startsWith("zh") ? "zh" : "en";
}

function t(key) {
  return (I18N[uiLang] && I18N[uiLang][key]) || I18N.en[key] || key;
}

function applyI18n() {
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    const val = t(key);
    if (typeof val === "string") el.textContent = val;
  });
  document.title = t("appTitle");
  document.querySelectorAll("#uiLangSwitch button").forEach((btn) => {
    btn.classList.toggle("on", btn.getAttribute("data-ui-lang") === uiLang);
  });
  renderStepNav();
  paintSlots();
}

function readLocalPrefs() {
  try {
    return JSON.parse(localStorage.getItem(PREF_KEY) || "{}");
  } catch {
    return {};
  }
}

function writeLocalPrefs(partial) {
  const next = { ...readLocalPrefs(), ...partial };
  localStorage.setItem(PREF_KEY, JSON.stringify(next));
  if (document.getElementById("remember").checked) {
    fetch("/api/prefs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prefs: next }),
    }).catch(() => {});
  }
}

function setTheme(theme) {
  const value = theme === "light" ? "light" : "gold";
  document.documentElement.setAttribute("data-theme", value);
  const sw = document.getElementById("themeSwitch");
  if (sw) sw.dataset.on = value;
  writeLocalPrefs({ theme: value });
}

function hideAllStages() {
  for (let i = 0; i <= LAST; i++) {
    document.getElementById("stage" + i)?.classList.remove("on");
  }
}

function goStep(n) {
  currentStep = n;
  hideAllStages();
  document.getElementById("stage" + n)?.classList.add("on");
  renderStepNav();
  applyI18n();
  persistForm();
  if (n === 4) ensureLookPreview();
  else if (window.GRDPreview) window.GRDPreview.unmountLookPreview();
}

function renderStepNav() {
  const nav = document.getElementById("stepNav");
  const labels = t("steps");
  nav.innerHTML = labels
    .map((label, i) => {
      const cls = i === currentStep ? "on" : i < currentStep ? "done" : "";
      return `<button type="button" class="step-pill ${cls}" data-step="${i}">${String(i + 1).padStart(2, "0")} ${label}</button>`;
    })
    .join("");
  nav.querySelectorAll("button").forEach((btn) => {
    btn.addEventListener("click", () => goStep(Number(btn.dataset.step)));
  });
}

function log(msg) {
  const dock = document.getElementById("logDock");
  const line = document.createElement("div");
  line.textContent = new Date().toLocaleTimeString() + "  " + msg;
  dock.prepend(line);
}

function assetKind(slotId) {
  if ((catalog.audio || []).some((s) => s.id === slotId)) return "audio";
  if ((catalog.images || []).some((s) => s.id === slotId)) return "image";
  return "model";
}

function assetUrl(slotId) {
  return "/api/asset/" + encodeURIComponent(slotId) + "?v=" + (replaced.has(slotId) ? Date.now() : "stock");
}

function slotCard(slot) {
  const isOn = replaced.has(slot.id);
  const label = uiLang === "zh" ? slot.label_zh : slot.label_en;
  const kind = assetKind(slot.id);
  const preview =
    kind === "image"
      ? `<img class="thumb" alt="" src="${assetUrl(slot.id)}" />`
      : "";
  const extra =
    kind === "audio"
      ? `<button class="soft" type="button" data-act="play">${t("preview")}</button>`
      : kind === "model"
        ? `<button class="soft" type="button" data-act="view">${t("view3d")}</button>`
        : "";
  return `<article class="slot ${isOn ? "replaced" : ""}" data-slot="${slot.id}" data-kind="${kind}">
    <h3>${label}</h3>
    <div class="meta">${slot.path}<br/>${isOn ? t("replaced") : t("stock")}</div>
    ${preview}
    <input type="file" accept="${slot.accept}" hidden />
    <div class="actions" style="padding-top:8px">
      ${extra}
      <button class="soft" type="button" data-act="pick">${t("replace")}</button>
      <button class="ghost" type="button" data-act="clear">${t("clear")}</button>
    </div>
  </article>`;
}

function paintSlots() {
  const map = [
    ["audioSlots", catalog.audio],
    ["imageSlots", catalog.images],
    ["modelSlots", catalog.models],
  ];
  map.forEach(([id, list]) => {
    const root = document.getElementById(id);
    if (!root) return;
    root.innerHTML = (list || []).map(slotCard).join("");
    root.querySelectorAll(".slot").forEach(bindSlot);
  });
}

function stopAudio() {
  if (playing) {
    playing.pause();
    playing.src = "";
    playing = null;
  }
}

function bindSlot(card) {
  const slotId = card.dataset.slot;
  const file = card.querySelector('input[type="file"]');
  card.querySelector('[data-act="pick"]').addEventListener("click", () => file.click());
  card.querySelector('[data-act="clear"]').addEventListener("click", async () => {
    await fetch("/api/upload/" + slotId, { method: "DELETE" });
    replaced.delete(slotId);
    paintSlots();
    persistForm();
  });
  const playBtn = card.querySelector('[data-act="play"]');
  if (playBtn) {
    playBtn.addEventListener("click", () => {
      if (playing && playBtn.dataset.on === "1") {
        stopAudio();
        playBtn.dataset.on = "0";
        playBtn.textContent = t("preview");
        return;
      }
      stopAudio();
      document.querySelectorAll('[data-act="play"]').forEach((b) => {
        b.dataset.on = "0";
        b.textContent = t("preview");
      });
      const audio = new Audio(assetUrl(slotId));
      playing = audio;
      playBtn.dataset.on = "1";
      playBtn.textContent = t("stop");
      audio.addEventListener("ended", () => {
        playBtn.dataset.on = "0";
        playBtn.textContent = t("preview");
        if (playing === audio) playing = null;
      });
      audio.play().catch((err) => log(String(err)));
    });
  }
  const viewBtn = card.querySelector('[data-act="view"]');
  if (viewBtn) {
    viewBtn.addEventListener("click", () => openModelModal(slotId, card.querySelector("h3").textContent));
  }
  file.addEventListener("change", async () => {
    if (!file.files || !file.files[0]) return;
    const body = new FormData();
    body.append("file", file.files[0]);
    const res = await fetch("/api/upload/" + slotId, { method: "POST", body });
    const data = await res.json();
    if (data.ok) {
      replaced = new Set(data.replaced || []);
      log(slotId + " ← " + file.files[0].name);
      paintSlots();
      persistForm();
    }
  });
}

function paintSceneFields(scene) {
  const root = document.getElementById("sceneFields");
  root.innerHTML = SCENE_FIELDS.map(([key, label, type]) => {
    const val = scene[key] ?? "";
    return `<label>${label}<input id="sc_${key}" type="${type}" ${type === "number" ? 'step="any"' : ""} value="${val}" /></label>`;
  }).join("");
  root.querySelectorAll("input").forEach((el) => {
    el.addEventListener("input", () => {
      if (window.GRDPreview) window.GRDPreview.updateLookPreview(collectScene());
      persistForm();
    });
  });
  ensureLookPreview();
}

function ensureLookPreview() {
  const host = document.getElementById("lookView");
  if (!host || currentStep !== 4) return;
  const api = window.GRDPreview;
  if (!api) {
    host.innerHTML = '<div class="model-status">Loading renderer…</div>';
    setTimeout(ensureLookPreview, 250);
    return;
  }
  api.mountLookPreview(host, collectScene());
}

function collectScene() {
  const scene = {};
  SCENE_FIELDS.forEach(([key, , type]) => {
    const el = document.getElementById("sc_" + key);
    if (!el) return;
    scene[key] = type === "number" ? Number(el.value) : el.value;
  });
  return scene;
}

function collectProject() {
  return {
    title: document.getElementById("pageTitle").value.trim() || "原神启动",
    folderName: document.getElementById("folderName").value.trim() || "genshin-replica-export",
    exportDir: (document.getElementById("exportDir")?.value || "").trim(),
    scene: collectScene(),
    hudTime: document.getElementById("hudTime").checked,
    hudRegion: document.getElementById("hudRegion").checked,
    hudWeather: document.getElementById("hudWeather").checked,
    disclaimerMode: document.querySelector('input[name="discMode"]:checked')?.value || "original",
    disclaimerText: document.getElementById("disclaimerText").value,
    remember: document.getElementById("remember").checked,
  };
}

function applyProject(project) {
  document.getElementById("pageTitle").value = project.title || "原神启动";
  document.getElementById("folderName").value = project.folderName || "genshin-replica-export";
  if (document.getElementById("exportDir") && project.exportDir) {
    document.getElementById("exportDir").value = project.exportDir;
  }
  if (document.getElementById("exportFolderName")) {
    document.getElementById("exportFolderName").value = project.folderName || "genshin-replica-export";
  }
  document.getElementById("hudTime").checked = !!project.hudTime;
  document.getElementById("hudRegion").checked = !!project.hudRegion;
  document.getElementById("hudWeather").checked = !!project.hudWeather;
  document.getElementById("remember").checked = project.remember !== false;
  const mode = project.disclaimerMode || "original";
  document.querySelectorAll('input[name="discMode"]').forEach((el) => {
    el.checked = el.value === mode;
  });
  document.getElementById("disclaimerText").value = project.disclaimerText || "";
  paintSceneFields(project.scene || catalog.defaults.scene || {});
}

async function persistForm() {
  const project = collectProject();
  if (!project.remember) return;
  writeLocalPrefs({
    theme: document.documentElement.getAttribute("data-theme") || "gold",
    title: project.title,
    folderName: project.folderName,
    exportDir: project.exportDir,
    hudTime: project.hudTime,
    hudRegion: project.hudRegion,
    hudWeather: project.hudWeather,
    disclaimerMode: project.disclaimerMode,
  });
  await fetch("/api/project", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(project),
  });
}

async function boot() {
  uiLang = detectUiLang();
  const local = readLocalPrefs();
  setTheme(local.theme || "gold");

  const defaults = await fetch("/api/defaults").then((r) => r.json());
  document.getElementById("appVersion").textContent = "v" + (defaults.version || "1.0.0");
  log(defaults.vendorReady ? t("vendorOk") : t("vendorMissing"));

  const cat = await fetch("/api/catalog").then((r) => r.json());
  catalog = cat;
  replaced = new Set(cat.replaced || []);
  const proj = await fetch("/api/project").then((r) => r.json());
  applyProject(proj.project || cat.defaults);
  if (!document.getElementById("exportDir").value) {
    document.getElementById("exportDir").value = local.exportDir || defaults.exportDir || "";
  }
  if (local.title) document.getElementById("pageTitle").value = local.title;
  if (typeof local.hudTime === "boolean") document.getElementById("hudTime").checked = local.hudTime;
  if (typeof local.hudRegion === "boolean") document.getElementById("hudRegion").checked = local.hudRegion;
  if (typeof local.hudWeather === "boolean") document.getElementById("hudWeather").checked = local.hudWeather;

  applyI18n();
  goStep(0);

  document.getElementById("themeGold").addEventListener("click", () => setTheme("gold"));
  document.getElementById("themeLight").addEventListener("click", () => setTheme("light"));
  document.querySelectorAll("#uiLangSwitch button").forEach((btn) => {
    btn.addEventListener("click", () => {
      uiLang = btn.getAttribute("data-ui-lang");
      localStorage.setItem("aio.uiLang", uiLang);
      applyI18n();
    });
  });
  document.getElementById("next0").addEventListener("click", () => goStep(1));
  document.getElementById("next1").addEventListener("click", () => goStep(2));
  document.getElementById("next2").addEventListener("click", () => goStep(3));
  document.getElementById("next3").addEventListener("click", () => goStep(4));
  document.getElementById("next4").addEventListener("click", () => goStep(5));
  document.getElementById("next5").addEventListener("click", () => goStep(6));
  document.querySelectorAll("[data-back]").forEach((btn) => {
    btn.addEventListener("click", () => goStep(Number(btn.getAttribute("data-back"))));
  });
  document.getElementById("exportBtn").addEventListener("click", openExportModal);
  document.getElementById("exportCancel").addEventListener("click", closeExportModal);
  document.getElementById("exportConfirm").addEventListener("click", confirmExport);
  document.getElementById("browseDir").addEventListener("click", browseExportDir);
  document.getElementById("modelModalClose").addEventListener("click", closeModelModal);
  document.getElementById("modelModal").addEventListener("click", (ev) => {
    if (ev.target.id === "modelModal") closeModelModal();
  });
  document.getElementById("exportModal").addEventListener("click", (ev) => {
    if (ev.target.id === "exportModal") closeExportModal();
  });
  ["pageTitle", "folderName", "disclaimerText", "hudTime", "hudRegion", "hudWeather", "remember"].forEach((id) => {
    document.getElementById(id).addEventListener("change", persistForm);
  });
}

function openExportModal() {
  const folder = document.getElementById("folderName").value.trim() || "genshin-replica-export";
  document.getElementById("exportFolderName").value = folder;
  document.getElementById("exportModalHint").textContent = "";
  document.getElementById("exportModal").hidden = false;
}

function closeExportModal() {
  document.getElementById("exportModal").hidden = true;
}

async function browseExportDir() {
  try {
    const res = await fetch("/api/pick-folder", { method: "POST" });
    const data = await res.json();
    if (data.path) {
      document.getElementById("exportDir").value = data.path;
      persistForm();
      return;
    }
    document.getElementById("exportModalHint").textContent = t("pickFail");
    if (!document.getElementById("exportDir").value && data.fallback) {
      document.getElementById("exportDir").value = data.fallback;
    }
  } catch (err) {
    document.getElementById("exportModalHint").textContent = t("pickFail");
    log(String(err));
  }
}

async function confirmExport() {
  const destDir = document.getElementById("exportDir").value.trim();
  const folderName = document.getElementById("exportFolderName").value.trim() || "genshin-replica-export";
  if (!destDir) {
    document.getElementById("exportModalHint").textContent = t("pickFail");
    return;
  }
  document.getElementById("folderName").value = folderName;
  await persistForm();
  const hint = document.getElementById("exportHint");
  const modalHint = document.getElementById("exportModalHint");
  modalHint.textContent = "…";
  try {
    const res = await fetch("/api/export", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ destDir, folderName }),
    });
    const raw = await res.text();
    let data = {};
    try {
      data = raw ? JSON.parse(raw) : {};
    } catch {
      throw new Error((raw || res.statusText || t("exportFail")).slice(0, 180));
    }
    if (!res.ok || !data.ok) throw new Error(data.detail || raw || t("exportFail"));
    const msg = t("exported") + (data.saved ? "  " + t("savedTo") + " " + data.saved : "");
    hint.textContent = msg;
    modalHint.textContent = msg;
    log("export pristine=" + data.pristine + " saved=" + (data.saved || ""));
    closeExportModal();
    window.location.href = data.download || "/api/export/download";
  } catch (err) {
    modalHint.textContent = t("exportFail") + ": " + err.message;
    hint.textContent = t("exportFail") + ": " + err.message;
    log(String(err));
  }
}

async function openModelModal(slotId, title) {
  document.getElementById("modelModalTitle").textContent = title || slotId;
  document.getElementById("modelModal").hidden = false;
  const host = document.getElementById("modelView");
  host.innerHTML = "";
  const api = window.GRDPreview;
  if (!api) {
    host.textContent = "Three.js preview failed to load.";
    return;
  }
  await api.openModelPreview(host, assetUrl(slotId));
}

function closeModelModal() {
  window.GRDPreview && window.GRDPreview.closeModelPreview();
  document.getElementById("modelModal").hidden = true;
}

boot();
