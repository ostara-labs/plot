<script lang="ts">
	import { afterNavigate } from '$app/navigation';
	import { shouldRedirect } from '$lib/paraglide/runtime';
	import { onMount } from 'svelte';
	import '../app.css';

	let { children } = $props();

	/**
	 * Re-sync the URL after client-side navigations (Paraglide docs): a
	 * locale-changing URL must load a new document so `<html lang>`, server
	 * data and client state all match. The initial SSR request is already
	 * canonicalized by `paraglideMiddleware` in hooks.server.ts.
	 */
	async function syncLocaleUrl(url: string) {
		const decision = await shouldRedirect({ url });
		if (decision.shouldRedirect && decision.redirectUrl) {
			window.location.href = decision.redirectUrl.href;
		}
	}

	onMount(() => {
		void syncLocaleUrl(window.location.href);
	});

	afterNavigate((navigation) => {
		if (navigation.to) {
			void syncLocaleUrl(navigation.to.url.href);
		}
	});
</script>

{@render children()}
