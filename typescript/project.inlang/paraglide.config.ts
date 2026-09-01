import { defineConfig } from "@inlang/paraglide-js";

/**
 * Paraglide JS compiler options — shared by the CLI (`paraglide-js compile`)
 * and the Vite plugin. Lives inside the inlang project so both read it.
 *
 * Locale detection order (spec wave-01 §3): URL prefix wins (routing by
 * /fr and /en), then Accept-Language, then the `PARAGLIDE_LOCALE` cookie,
 * then FR as the base locale. The `urlPatterns` below prefix ALL locales
 * (SvelteKit models locale-aware routes with a required `[locale]` segment),
 * so an unprefixed path like `/` falls through to the other strategies and
 * the middleware redirects to `/fr` or `/en`.
 */
export default defineConfig({
  outdir: "./src/lib/paraglide",
  emitTsDeclarations: true,
  strategy: ["url", "preferredLanguage", "cookie", "baseLocale"],
  urlPatterns: [
    {
      pattern: "/",
      localized: [
        ["fr", "/fr"],
        ["en", "/en"],
      ],
    },
    {
      pattern: "/:path(.*)?",
      localized: [
        ["fr", "/fr/:path(.*)?"],
        ["en", "/en/:path(.*)?"],
      ],
    },
  ],
});
