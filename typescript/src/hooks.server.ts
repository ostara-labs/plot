import type { Handle } from "@sveltejs/kit";
import { getTextDirection } from "$lib/paraglide/runtime";
import { paraglideMiddleware } from "$lib/paraglide/server";

/**
 * Paraglide middleware (spec wave-01 §3): locale detection from URL prefix
 * (/fr, /en), then Accept-Language, then cookie, then FR default. Unprefixed
 * document requests are 307-redirected to the canonical localized URL.
 *
 * The original `event` is passed to `resolve` (not the delocalized request):
 * routes are modeled with a required `[locale]` segment, so SvelteKit must
 * see the localized URL to match `src/routes/[locale]/+page.svelte`.
 */
const paraglideHandle: Handle = ({ event, resolve }) =>
  paraglideMiddleware(event.request, ({ locale }) => {
    return resolve(event, {
      transformPageChunk: ({ html }) => {
        return html.replace("%lang%", locale).replace("%dir%", getTextDirection(locale));
      },
    });
  });

export const handle: Handle = paraglideHandle;
