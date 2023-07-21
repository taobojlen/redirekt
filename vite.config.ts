import { defineConfig } from "vite";

export default defineConfig({
  build: {
    outDir: "frontend/dist",
    rollupOptions: {
      input: {
        "index.ts": "./frontend/index.ts",
      },
    },
  },
  server: {
    port: 3000,
    origin: "http://localhost:8000",
  },
  preview: {
    port: 3000,
  },
  base: "/static/",
});
