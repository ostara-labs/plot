<script lang="ts">
	import { page } from '$app/state';
	import LanguageSwitcher from '$lib/components/LanguageSwitcher.svelte';
	import * as m from '$lib/paraglide/messages';
	import { localizeHref } from '$lib/paraglide/runtime';

	let { children } = $props();

	const locale = $derived(page.params.locale as 'fr' | 'en');
</script>

<header class="app-header">
	<a class="app-header__brand" href={localizeHref('/', { locale })}>Plot</a>
	<LanguageSwitcher />
</header>

<main class="app-main">
	{@render children()}
</main>

<footer class="app-footer">
	<p>{m['status.scaffold']()}</p>
</footer>

<style>
	.app-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 1rem 1.5rem;
		border-bottom: 1px solid var(--color-surface-300);
	}

	.app-header__brand {
		font-weight: 700;
		font-size: 1.25rem;
		text-decoration: none;
		color: var(--color-primary-500);
	}

	.app-main {
		min-height: calc(100vh - 8rem);
	}

	.app-footer {
		padding: 1rem 1.5rem;
		border-top: 1px solid var(--color-surface-300);
		font-size: 0.875rem;
		color: var(--color-surface-700);
	}
</style>
