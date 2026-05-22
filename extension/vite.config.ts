import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const fromRoot = (relativePath: string) => new URL(relativePath, import.meta.url).pathname;

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": fromRoot("./src")
    }
  },
  build: {
    outDir: "dist",
    emptyOutDir: true,
    sourcemap: true,
    rollupOptions: {
      input: {
        options: fromRoot("./options.html"),
        background: fromRoot("./src/background/index.ts"),
        content: fromRoot("./src/content/index.ts"),
        injected: fromRoot("./src/injected/index.ts")
      },
      output: {
        entryFileNames: "[name].js",
        chunkFileNames: "chunks/[name]-[hash].js",
        assetFileNames: "assets/[name]-[hash][extname]"
      }
    }
  }
});
