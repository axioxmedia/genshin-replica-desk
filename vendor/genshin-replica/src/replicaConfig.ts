export type ReplicaConfig = {
  fogColor?: string;
  fogNear?: number;
  fogFar?: number;
  ambientColor?: string;
  ambientIntensity?: number;
  dirColor?: string;
  dirIntensity?: number;
  bgColor1?: string;
  bgColor2?: string;
  bgColor3?: string;
  bgStop1?: number;
  bgStop2?: number;
  cameraFov?: number;
  cameraTilt?: number;
  disclaimer?: string;
};

declare global {
  interface Window {
    __REPLICA_CONFIG__?: ReplicaConfig;
  }
}

export function replicaConfig(): ReplicaConfig {
  return window.__REPLICA_CONFIG__ || {};
}

export function hexNum(value: string | undefined, fallback: number): number {
  if (!value) return fallback;
  const raw = value.trim().replace("#", "");
  if (!/^[0-9a-fA-F]{6}$/.test(raw)) return fallback;
  return parseInt(raw, 16);
}
