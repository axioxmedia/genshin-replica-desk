import { defineConfig } from "vite";

import glsl from "vite-plugin-glsl";

export default defineConfig({
  base: "./",
  server: {
    open: true,
  },
  plugins: [glsl()],
});
