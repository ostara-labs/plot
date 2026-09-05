<script lang="ts">
	import MapShell from '$lib/components/MapShell.svelte';
	import * as m from '$lib/paraglide/messages';
</script>

<svelte:head>
	<title>{m['home.title']()}</title>
</svelte:head>

<section class="hero">
	<h1 class="hero__title">{m['home.title']()}</h1>
	<p class="hero__subtitle">{m['home.subtitle']()}</p>
	<button class="btn btn-filled" type="button">{m['project.new_button']()}</button>
</section>

<section class="projects">
	<h2 class="projects__title">{m['project.list_title']()}</h2>
	<p class="projects__empty">{m['project.list_empty']()}</p>
</section>

<section class="map" aria-label={m['home.map_placeholder']()}>
	<MapShell />
</section>

<style>
	.hero {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
		text-align: center;
		padding: 4rem 1.5rem 2rem;
	}

	.hero__title {
		font-size: 2.5rem;
		font-weight: 800;
		line-height: 1.1;
		max-width: 24ch;
	}

	.hero__subtitle {
		font-size: 1.125rem;
		color: var(--color-surface-700);
		max-width: 48ch;
	}

	.projects {
		padding: 2rem 1.5rem;
	}

	.projects__title {
		font-size: 1.5rem;
		font-weight: 700;
		margin-bottom: 0.5rem;
	}

	.projects__empty {
		color: var(--color-surface-700);
	}

	.map {
		padding: 0 1.5rem 3rem;
	}
</style>
