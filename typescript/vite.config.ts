import { paraglideVitePlugin } from "@inlang/paraglide-js";
import { sveltekit } from "@sveltejs/kit/vite";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [
    tailwindcss(),
    sveltekit(),
    // Compiler options (outdir, strategy, urlPatterns) live in
    // project.inlang/paraglide.config.ts — shared with the CLI.
    paraglideVitePlugin({ project: "./project.inlang" }),
  ],
});
