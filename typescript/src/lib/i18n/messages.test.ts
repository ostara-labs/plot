import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";
import { flattenMessages } from "./check";

const messagesDir = resolve(import.meta.dirname, "../../../messages");

function readJson(file: string): Record<string, unknown> {
  return JSON.parse(readFileSync(resolve(messagesDir, file), "utf8")) as Record<string, unknown>;
}

/**
 * Smoke test: the message files parse and expose the keys the scaffold UI
 * actually renders. Guards against a broken i18n pipeline (empty files,
 * renamed keys, non-string values) without needing a browser.
 */
describe("messages smoke test", () => {
  const fr = readJson("fr.json");
  const en = readJson("en.json");

  it("both message files are non-empty", () => {
    expect(Object.keys(flattenMessages(fr)).length).toBeGreaterThan(0);
    expect(Object.keys(flattenMessages(en)).length).toBeGreaterThan(0);
  });

  it("all values are non-empty strings", () => {
    for (const [key, value] of Object.entries(flattenMessages(fr))) {
      expect(value.trim().length, `fr key "${key}" is empty`).toBeGreaterThan(0);
    }
    for (const [key, value] of Object.entries(flattenMessages(en))) {
      expect(value.trim().length, `en key "${key}" is empty`).toBeGreaterThan(0);
    }
  });

  it("exposes the keys used by the home page", () => {
    const frKeys = Object.keys(flattenMessages(fr));
    for (const key of ["home.title", "home.subtitle", "project.new_button", "project.list_title"]) {
      expect(frKeys).toContain(key);
    }
  });
});
