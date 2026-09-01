<script lang="ts">
	import { page } from '$app/state';
	import * as m from '$lib/paraglide/messages';
	import { locales, localizeHref } from '$lib/paraglide/runtime';

	const current = $derived(page.params.locale);

	/**
	 * FR/EN selector (spec wave-01 §3). Locale changes are full document
	 * navigations (`data-sveltekit-reload`) so `<html lang>`, server-rendered
	 * data and client state all match the new locale.
	 */
	function label(locale: string): string {
		return locale === 'fr' ? m['language.fr']() : m['language.en']();
	}
</script>

<nav class="language-switcher" aria-label={m['language.switch']()}>
	{#each locales as locale}
		<a
			class="language-switcher__link"
			class:language-switcher__link--active={locale === current}
			href={localizeHref(page.url.pathname, { locale })}
			aria-current={locale === current ? 'true' : undefined}
			data-sveltekit-reload
		>
			{label(locale)}
		</a>
	{/each}
</nav>

<style>
	.language-switcher {
		display: flex;
		gap: 0.5rem;
	}

	.language-switcher__link {
		padding: 0.375rem 0.75rem;
		border-radius: var(--radius-full);
		border: 1px solid var(--color-surface-300);
		background: var(--color-surface-100);
		color: var(--color-surface-700);
		font-size: 0.875rem;
		font-weight: 600;
		text-decoration: none;
		transition:
			border-color 150ms ease,
			background 150ms ease;
	}

	.language-switcher__link:hover {
		border-color: var(--color-surface-500);
	}

	.language-switcher__link--active {
		background: var(--color-primary-500);
		border-color: var(--color-primary-500);
		color: var(--color-on-primary);
	}
</style>
