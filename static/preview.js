import * as THREE from "/assets/vendor/three/three.module.js";
import { OrbitControls } from "/assets/vendor/three/examples/jsm/controls/OrbitControls.js";
import { GLTFLoader } from "/assets/vendor/three/examples/jsm/loaders/GLTFLoader.js";
import { DRACOLoader } from "/assets/vendor/three/examples/jsm/loaders/DRACOLoader.js";

const draco = new DRACOLoader();
draco.setDecoderPath("/assets/vendor/three/examples/jsm/libs/draco/gltf/");
const loader = new GLTFLoader();
loader.setDRACOLoader(draco);
const modelCache = new Map();

let modal = null;
let look = null;

function disposeObject(root) {
  if (!root) return;
  root.traverse((obj) => {
    if (obj.geometry) obj.geometry.dispose();
    const mat = obj.material;
    if (!mat) return;
    const list = Array.isArray(mat) ? mat : [mat];
    list.forEach((m) => {
      Object.values(m).forEach((v) => {
        if (v && v.isTexture) v.dispose();
      });
      m.dispose();
    });
  });
}

function frameObject(root, camera, controls) {
  const box = new THREE.Box3().setFromObject(root);
  const size = box.getSize(new THREE.Vector3());
  const center = box.getCenter(new THREE.Vector3());
  const radius = Math.max(size.length() * 0.5, 1);
  root.position.sub(center);
  camera.position.set(radius * 0.35, radius * 0.22, radius * 0.7);
  camera.near = Math.max(radius / 800, 0.05);
  camera.far = radius * 40;
  camera.updateProjectionMatrix();
  if (controls) {
    controls.target.set(0, 0, 0);
    controls.update();
  }
}

async function loadGltf(url) {
  if (modelCache.has(url)) return modelCache.get(url).clone();
  const gltf = await loader.loadAsync(url);
  modelCache.set(url, gltf.scene);
  return gltf.scene.clone();
}

function makeSkyDome() {
  const geo = new THREE.SphereGeometry(800, 48, 32);
  const mat = new THREE.ShaderMaterial({
    side: THREE.BackSide,
    depthWrite: false,
    uniforms: {
      uColor1: { value: new THREE.Color("#001c54") },
      uColor2: { value: new THREE.Color("#023fa1") },
      uColor3: { value: new THREE.Color("#26a8ff") },
      uStop1: { value: 0.2 },
      uStop2: { value: 0.6 },
    },
    vertexShader: `
      varying vec3 vDir;
      void main() {
        vDir = normalize(position);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      varying vec3 vDir;
      uniform vec3 uColor1;
      uniform vec3 uColor2;
      uniform vec3 uColor3;
      uniform float uStop1;
      uniform float uStop2;
      void main() {
        float h = clamp(vDir.y * 0.5 + 0.5, 0.0, 1.0);
        vec3 col = mix(uColor3, uColor2, smoothstep(0.0, uStop1 + 0.001, h));
        col = mix(col, uColor1, smoothstep(uStop1, max(uStop2, uStop1 + 0.02), h));
        gl_FragColor = vec4(col, 1.0);
      }
    `,
  });
  return new THREE.Mesh(geo, mat);
}

function applyLookParams(state, params) {
  if (!state) return;
  const p = params || {};
  state.scene.fog.color.set(p.fogColor || "#389af2");
  state.scene.fog.near = Math.max(8, Number(p.fogNear) || 5000) / 80;
  state.scene.fog.far = Math.max(20, Number(p.fogFar) || 10000) / 55;
  state.ambient.color.set(p.ambientColor || "#0f6eff");
  state.ambient.intensity = Math.max(0.2, (Number(p.ambientIntensity) || 6) * 0.35);
  state.key.color.set(p.dirColor || "#ff6222");
  state.key.intensity = Math.max(0.2, (Number(p.dirIntensity) || 35) * 0.06);
  const sky = state.sky.material;
  sky.uniforms.uColor1.value.set(p.bgColor1 || "#001c54");
  sky.uniforms.uColor2.value.set(p.bgColor2 || "#023fa1");
  sky.uniforms.uColor3.value.set(p.bgColor3 || "#26a8ff");
  sky.uniforms.uStop1.value = Number(p.bgStop1 ?? 0.2);
  sky.uniforms.uStop2.value = Number(p.bgStop2 ?? 0.6);
  state.camera.fov = Number(p.cameraFov) || 45;
  state.camera.rotation.x = THREE.MathUtils.degToRad(Number(p.cameraTilt) || 5.5);
  state.camera.updateProjectionMatrix();
}

function bootRenderer(host, width, height) {
  const scene = new THREE.Scene();
  scene.fog = new THREE.Fog("#389af2", 40, 180);
  const camera = new THREE.PerspectiveCamera(45, width / Math.max(height, 1), 0.1, 4000);
  camera.position.set(6, 3.2, 14);
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setSize(width, height);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  host.innerHTML = "";
  host.appendChild(renderer.domElement);
  return { scene, camera, renderer };
}

export function closeModelPreview() {
  if (!modal) return;
  if (modal.frame) cancelAnimationFrame(modal.frame);
  disposeObject(modal.scene);
  modal.renderer.dispose();
  modal = null;
}

export async function openModelPreview(container, url) {
  closeModelPreview();
  const width = Math.max(320, container.clientWidth || 640);
  const height = Math.max(240, container.clientHeight || 420);
  const status = document.createElement("div");
  status.className = "model-status";
  status.textContent = "Loading…";
  const { scene, camera, renderer } = bootRenderer(container, width, height);
  container.appendChild(status);
  scene.background = new THREE.Color(0x8ec7ff);
  scene.add(new THREE.HemisphereLight(0xb8e0ff, 0x6a4a2a, 1.1));
  const key = new THREE.DirectionalLight(0xfff1d6, 2.2);
  key.position.set(8, 18, 10);
  scene.add(key);
  const ground = new THREE.Mesh(
    new THREE.CircleGeometry(40, 48),
    new THREE.MeshStandardMaterial({ color: 0xd6e7f7, roughness: 0.9 })
  );
  ground.rotation.x = -Math.PI / 2;
  ground.position.y = -0.02;
  scene.add(ground);
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  modal = { scene, camera, renderer, controls, frame: 0 };
  try {
    const root = await loadGltf(url);
    scene.add(root);
    frameObject(root, camera, controls);
    status.remove();
  } catch (err) {
    status.textContent = String(err && err.message ? err.message : err);
  }
  const tick = () => {
    if (!modal) return;
    modal.frame = requestAnimationFrame(tick);
    modal.controls.update();
    modal.renderer.render(modal.scene, modal.camera);
  };
  tick();
}

export function unmountLookPreview() {
  if (!look) return;
  if (look.frame) cancelAnimationFrame(look.frame);
  disposeObject(look.scene);
  look.renderer.dispose();
  look = null;
}

export async function mountLookPreview(host, params) {
  if (look && look.host === host) {
    applyLookParams(look, params);
    return;
  }
  unmountLookPreview();
  const width = Math.max(280, host.clientWidth || 640);
  const height = Math.max(220, host.clientHeight || 420);
  const { scene, camera, renderer } = bootRenderer(host, width, height);
  const sky = makeSkyDome();
  scene.add(sky);
  const ambient = new THREE.AmbientLight(0x0f6eff, 2.1);
  const key = new THREE.DirectionalLight(0xff6222, 2.1);
  key.position.set(18, 28, 12);
  scene.add(ambient, key);
  const group = new THREE.Group();
  scene.add(group);
  look = {
    host,
    scene,
    camera,
    renderer,
    sky,
    ambient,
    key,
    group,
    frame: 0,
    spin: 0,
  };
  applyLookParams(look, params);
  const slots = [
    ["SM_ZhuZi01", [0, 0, 0], 0.1],
    ["SM_ZhuZi02", [12, 0, -9], 0.1],
    ["SM_ZhuZi03", [-12, 0, -7], 0.1],
    ["SM_ZhuZi04", [6, 0, 8], 0.1],
    ["SM_Qiao01", [4, 0, 10], 0.1],
    ["SM_Road", [0, 0, 4], 0.1],
    ["SM_BigCloud", [0, 18, -24], 0.08],
  ];
  const status = document.createElement("div");
  status.className = "model-status";
  status.textContent = "Loading scene…";
  host.appendChild(status);
  try {
    for (const [id, pos, scale] of slots) {
      const mesh = await loadGltf("/api/asset/" + id + "?v=look");
      mesh.position.set(pos[0], pos[1], pos[2]);
      mesh.scale.multiplyScalar(scale);
      group.add(mesh);
    }
    frameObject(group, camera, null);
    camera.position.y += 2.2;
    status.remove();
  } catch (err) {
    status.textContent = String(err && err.message ? err.message : err);
  }
  const tick = () => {
    if (!look) return;
    look.frame = requestAnimationFrame(tick);
    look.spin += 0.0016;
    look.group.rotation.y = Math.sin(look.spin) * 0.18;
    look.renderer.render(look.scene, look.camera);
  };
  tick();
}

export function updateLookPreview(params) {
  applyLookParams(look, params);
}

window.GRDPreview = {
  openModelPreview,
  closeModelPreview,
  mountLookPreview,
  updateLookPreview,
  unmountLookPreview,
};
