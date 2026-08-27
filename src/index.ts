/**
 * Plot — find the best terrain to build your house.
 */

export interface Coordinates {
  readonly lat: number;
  readonly lng: number;
}

export interface Terrain {
  readonly id: string;
  readonly name: string;
  readonly coordinates: Coordinates;
  readonly areaSqm: number;
  readonly priceEur: number;
  readonly zone: "urbain" | "periurbain" | "rural";
  readonly buildable: boolean;
}

export interface ScoredTerrain extends Terrain {
  readonly score: number;
}

/**
 * Price per square meter.
 */
export function pricePerSqm(t: Terrain): number {
  return t.areaSqm > 0 ? t.priceEur / t.areaSqm : 0;
}

/**
 * Score a terrain from 0 (worst) to 100 (best) based on affordability and size.
 */
export function score(t: Terrain, budget: number): ScoredTerrain {
  const psm = pricePerSqm(t);
  const affordability = psm > 0 ? Math.min(budget / (psm * t.areaSqm), 1) : 0;
  const sizeFit = Math.min(t.areaSqm / 500, 1); // 500 sqm = ideal
  const buildableBonus = t.buildable ? 1 : 0;

  const raw = affordability * 40 + sizeFit * 30 + buildableBonus * 30;
  const score = Math.round(raw * 100) / 100;

  return { ...t, score };
}

/**
 * Rank terrains by score, best first.
 */
export function rank(terrains: readonly Terrain[], budget: number): readonly ScoredTerrain[] {
  return terrains.map((t) => score(t, budget)).sort((a, b) => b.score - a.score);
}
