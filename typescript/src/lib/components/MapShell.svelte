<script lang="ts">
	import type { Map as MapLibreMap } from 'maplibre-gl';
	import * as m from '$lib/paraglide/messages';
	import { onMount } from 'svelte';

	let container: HTMLDivElement;

	/**
	 * MapLibre GL JS shell (spec wave-01 §2). Placeholder only — no real
	 * tiles, no data layers, no user flows (decision 27.18). Renders a basic
	 * OSM raster style so the shell is visible. The library is imported
	 * dynamically inside onMount to keep SSR safe.
	 */
	onMount(() => {
		let map: MapLibreMap | undefined;
		void (async () => {
			const { default: maplibregl } = await import('maplibre-gl');
			map = new maplibregl.Map({
				container,
				style: {
					version: 8,
					sources: {
						osm: {
							type: 'raster',
							tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
							tileSize: 256,
							attribution: '© OpenStreetMap contributors',
						},
					},
					layers: [{ id: 'osm', type: 'raster', source: 'osm' }],
				},
				center: [2.2137, 46.2276], // France
				zoom: 5,
			});
		})();

		return () => {
			map?.remove();
		};
	});
</script>

<div class="map-shell" bind:this={container} role="img" aria-label={m['home.map_placeholder']()}>
	<span class="map-shell__label">{m['home.map_placeholder']()}</span>
</div>

<style>
	.map-shell {
		position: relative;
		height: 24rem;
		border-radius: var(--radius-container);
		overflow: hidden;
		border: 1px solid var(--color-surface-300);
	}

	.map-shell__label {
		position: absolute;
		top: 0.75rem;
		left: 50%;
		transform: translateX(-50%);
		z-index: 1;
		padding: 0.25rem 0.75rem;
		border-radius: var(--radius-full);
		background: var(--color-surface-100);
		color: var(--color-surface-700);
		font-size: 0.75rem;
		box-shadow: var(--shadow-md);
	}
</style>
