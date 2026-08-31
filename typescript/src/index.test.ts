import { describe, expect, it } from "vitest";
import { pricePerSqm, rank, score, type Terrain } from "./index.js";

const TERRAINS: readonly Terrain[] = [
  {
    id: "1",
    name: "Parcelle A",
    coordinates: { lat: 48.8566, lng: 2.3522 },
    areaSqm: 800,
    priceEur: 200_000,
    zone: "periurbain",
    buildable: true,
  },
  {
    id: "2",
    name: "Parcelle B",
    coordinates: { lat: 48.86, lng: 2.36 },
    areaSqm: 300,
    priceEur: 150_000,
    zone: "urbain",
    buildable: true,
  },
  {
    id: "3",
    name: "Parcelle C",
    coordinates: { lat: 48.87, lng: 2.37 },
    areaSqm: 1200,
    priceEur: 100_000,
    zone: "rural",
    buildable: false,
  },
];

describe("pricePerSqm", () => {
  it("computes price / area", () => {
    expect(pricePerSqm(TERRAINS[0])).toBe(250);
  });

  it("returns 0 for zero-area terrain", () => {
    const zero: Terrain = { ...TERRAINS[0], areaSqm: 0 };
    expect(pricePerSqm(zero)).toBe(0);
  });
});

describe("score", () => {
  it("returns a ScoredTerrain with a numeric score", () => {
    const s = score(TERRAINS[0], 300_000);
    expect(s.score).toBeGreaterThanOrEqual(0);
    expect(s.score).toBeLessThanOrEqual(100);
  });

  it("buildable terrain scores higher than non-buildable", () => {
    const buildable = score(TERRAINS[0], 300_000);
    const notBuildable = score(TERRAINS[2], 300_000);
    expect(buildable.score).toBeGreaterThan(notBuildable.score);
  });

  it("treats a zero-priced terrain as fully affordable", () => {
    const free: Terrain = { ...TERRAINS[0], priceEur: 0 };
    const unaffordable: Terrain = { ...TERRAINS[0], priceEur: 1_000_000 };
    expect(score(free, 300_000).score).toBeGreaterThan(score(unaffordable, 300_000).score);
  });
});

describe("rank", () => {
  it("sorts by score descending", () => {
    const ranked = rank(TERRAINS, 300_000);
    for (let i = 1; i < ranked.length; i++) {
      expect(ranked[i - 1].score).toBeGreaterThanOrEqual(ranked[i].score);
    }
  });

  it("returns all terrains", () => {
    expect(rank(TERRAINS, 300_000)).toHaveLength(TERRAINS.length);
  });
});
