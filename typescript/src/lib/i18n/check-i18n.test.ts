import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import { findMissingKeys, findMissingMeta, flattenMessages } from "./check";

const messagesDir = resolve(import.meta.dirname, "../../../messages");

function readJson(file: string): Record<string, unknown> {
  return JSON.parse(readFileSync(resolve(messagesDir, file), "utf8")) as Record<string, unknown>;
}

describe("flattenMessages", () => {
  it("flattens nested objects into dotted keys", () => {
    const flat = flattenMessages({ project: { new_button: "+ Nouveau projet" } });
    expect(flat).toEqual({ "project.new_button": "+ Nouveau projet" });
  });

  it("ignores the $schema metadata key", () => {
    // Bracket syntax: `$schema` is a JSON-Schema convention key, exempt from
    // the namingConvention rule (27.27).
    const flat = flattenMessages({ ["$schema"]: "https://example.com/schema", hello: "world" });
    expect(flat).toEqual({ hello: "world" });
  });
});

describe("i18n completeness (27.17)", () => {
  const fr = readJson("fr.json");
  const en = readJson("en.json");
  const meta = readJson("fr.meta.json");

  it("every FR key has an EN translation", () => {
    const missing = findMissingKeys(fr, en);
    expect(missing).toEqual([]);
  });

  it("every FR key has a complete fr.meta.json entry (context + usage)", () => {
    const missing = findMissingMeta(fr, meta);
    expect(missing).toEqual([]);
  });

  it("FR keys follow the snake_case convention (dots as namespace separators)", () => {
    const keys = Object.keys(flattenMessages(fr));
    for (const key of keys) {
      expect(key).toMatch(/^[a-z0-9]+(?:[._][a-z0-9]+)*$/);
    }
  });
});
