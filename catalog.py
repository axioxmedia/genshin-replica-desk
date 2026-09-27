"""Replaceable slots inside alphardex/genshin-replica."""

from __future__ import annotations

ORIGINAL_DISCLAIMER = (
    "免责声明：\n"
    "本网站是一个纯粹的技术示例，旨在展示和分享我们的技术能力。"
    "网站的设计和内容受到《原神》的启发，并尽可能地复制了《原神》的登录界面。"
    "我们对此表示敬意，并强调这个项目不是官方的《原神》产品，也没有与《原神》或其母公司miHoYo有任何关联。\n"
    "我们没有，也无意从这个项目中获得任何经济利益。"
    "这个网站的所有内容仅供学习和研究目的，以便让更多的人了解和熟悉webgl开发技术。\n"
    "如果miHoYo或任何有关方面认为这个项目侵犯了他们的权益，请联系我们，我们会立即采取行动。"
)

# ClickMe.png is the book button in the screenshot. It is never exported.
REMOVED_SLOT = {
    "id": "click_me",
    "path": "public/Genshin/ClickMe.png",
    "reason": "invalid book button",
}

AUDIO_SLOTS = [
    {"id": "bgm", "label_zh": "背景音乐", "label_en": "Background music", "path": "public/Genshin/BGM.mp3", "accept": "audio/*"},
    {"id": "sfx_click", "label_zh": "点击音效", "label_en": "Click sting", "path": "public/Genshin/Genshin Impact [Duang].mp3", "accept": "audio/*"},
    {"id": "sfx_door_out", "label_zh": "门出现", "label_en": "Door appear", "path": "public/Genshin/Genshin Impact [DoorComeout].mp3", "accept": "audio/*"},
    {"id": "sfx_door_in", "label_zh": "穿门", "label_en": "Door through", "path": "public/Genshin/Genshin Impact [DoorThrough].mp3", "accept": "audio/*"},
]

IMAGE_SLOTS = [
    {"id": "logo", "label_zh": "加载 Logo", "label_en": "Loader logo", "path": "public/Genshin/Genshin.png", "accept": "image/*"},
    {"id": "entry", "label_zh": "进入条", "label_en": "Enter bar", "path": "public/Genshin/Entry.png", "accept": "image/*"},
    {"id": "elements", "label_zh": "元素进度条", "label_en": "Element bar", "path": "public/Genshin/Elements.png", "accept": "image/*"},
    {"id": "mouse", "label_zh": "鼠标指针", "label_en": "Cursor", "path": "public/Genshin/T_Mouse.png", "accept": "image/*"},
    {"id": "skybox", "label_zh": "天空盒贴图", "label_en": "Skybox", "path": "public/textures/skybox.png", "accept": "image/*"},
    {"id": "tex_0061", "label_zh": "材质 Tex_0061", "label_en": "Tex_0061", "path": "public/Genshin/Login/Textures/Tex_0061.png", "accept": "image/*"},
    {"id": "tex_0062", "label_zh": "材质 Tex_0062", "label_en": "Tex_0062", "path": "public/Genshin/Login/Textures/Tex_0062.png", "accept": "image/*"},
    {"id": "tex_0063", "label_zh": "材质 Tex_0063", "label_en": "Tex_0063", "path": "public/Genshin/Login/Textures/Tex_0063.png", "accept": "image/*"},
    {"id": "tex_0067b", "label_zh": "材质 Tex_0067b", "label_en": "Tex_0067b", "path": "public/Genshin/Login/Textures/Tex_0067b.png", "accept": "image/*"},
    {"id": "tex_0071", "label_zh": "材质 Tex_0071", "label_en": "Tex_0071", "path": "public/Genshin/Login/Textures/Tex_0071.png", "accept": "image/*"},
    {"id": "tex_0075", "label_zh": "材质 Tex_0075", "label_en": "Tex_0075", "path": "public/Genshin/Login/Textures/Tex_0075.png", "accept": "image/*"},
    {"id": "tex_0077", "label_zh": "材质 Tex_0077", "label_en": "Tex_0077", "path": "public/Genshin/Login/Textures/Tex_0077.png", "accept": "image/*"},
]

MODEL_SLOTS = [
    {"id": "DOOR", "label_zh": "门 DOOR", "label_en": "Door", "path": "public/Genshin/Login/DOOR.glb", "accept": ".glb,.gltf,model/gltf-binary,model/gltf+json"},
    {"id": "SM_BigCloud", "label_zh": "大云", "label_en": "Big cloud", "path": "public/Genshin/Login/SM_BigCloud.glb", "accept": ".glb,.gltf,model/gltf-binary"},
    {"id": "SM_Light", "label_zh": "光柱模型", "label_en": "Light mesh", "path": "public/Genshin/Login/SM_Light.glb", "accept": ".glb,.gltf,model/gltf-binary"},
    {"id": "SM_Qiao01", "label_zh": "桥 01", "label_en": "Bridge 01", "path": "public/Genshin/Login/SM_Qiao01.glb", "accept": ".glb,.gltf,model/gltf-binary"},
    {"id": "SM_Qiao02", "label_zh": "桥 02", "label_en": "Bridge 02", "path": "public/Genshin/Login/SM_Qiao02.glb", "accept": ".glb,.gltf,model/gltf-binary"},
    {"id": "SM_Qiao03", "label_zh": "桥 03", "label_en": "Bridge 03", "path": "public/Genshin/Login/SM_Qiao03.glb", "accept": ".glb,.gltf,model/gltf-binary"},
    {"id": "SM_Qiao04", "label_zh": "桥 04", "label_en": "Bridge 04", "path": "public/Genshin/Login/SM_Qiao04.glb", "accept": ".glb,.gltf,model/gltf-binary"},
    {"id": "SM_Road", "label_zh": "路面", "label_en": "Road", "path": "public/Genshin/Login/SM_Road.glb", "accept": ".glb,.gltf,model/gltf-binary"},
    {"id": "SM_ZhuZi01", "label_zh": "柱 01", "label_en": "Column 01", "path": "public/Genshin/Login/SM_ZhuZi01.glb", "accept": ".glb,.gltf,model/gltf-binary"},
    {"id": "SM_ZhuZi02", "label_zh": "柱 02", "label_en": "Column 02", "path": "public/Genshin/Login/SM_ZhuZi02.glb", "accept": ".glb,.gltf,model/gltf-binary"},
    {"id": "SM_ZhuZi03", "label_zh": "柱 03", "label_en": "Column 03", "path": "public/Genshin/Login/SM_ZhuZi03.glb", "accept": ".glb,.gltf,model/gltf-binary"},
    {"id": "SM_ZhuZi04", "label_zh": "柱 04", "label_en": "Column 04", "path": "public/Genshin/Login/SM_ZhuZi04.glb", "accept": ".glb,.gltf,model/gltf-binary"},
    {"id": "WHITE_PLANE", "label_zh": "白平面", "label_en": "White plane", "path": "public/Genshin/Login/WHITE_PLANE.glb", "accept": ".glb,.gltf,model/gltf-binary"},
]

ALL_SLOTS = {s["id"]: s for s in AUDIO_SLOTS + IMAGE_SLOTS + MODEL_SLOTS}

DEFAULT_SCENE = {
    "pageTitle": "原神启动",
    "fogColor": "#389af2",
    "fogNear": 5000,
    "fogFar": 10000,
    "ambientColor": "#0f6eff",
    "ambientIntensity": 6,
    "dirColor": "#ff6222",
    "dirIntensity": 35,
    "bgColor1": "#001c54",
    "bgColor2": "#023fa1",
    "bgColor3": "#26a8ff",
    "bgStop1": 0.2,
    "bgStop2": 0.6,
    "cameraFov": 45,
    "cameraTilt": 5.5,
}

DEFAULT_PROJECT = {
    "title": "原神启动",
    "folderName": "genshin-replica-export",
    "exportDir": "",
    "scene": dict(DEFAULT_SCENE),
    "hudTime": False,
    "hudRegion": False,
    "hudWeather": False,
    "disclaimerMode": "original",
    "disclaimerText": ORIGINAL_DISCLAIMER,
    "remember": True,
}


def catalog_payload() -> dict:
    return {
        "audio": AUDIO_SLOTS,
        "images": IMAGE_SLOTS,
        "models": MODEL_SLOTS,
        "removed": REMOVED_SLOT,
        "defaults": DEFAULT_PROJECT,
    }
