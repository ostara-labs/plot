/**
 * i18n completeness gate (spec wave-01, decision 27.17).
 *
 * Fails (exit 1) when a key in `messages/fr.json` has no translation in
 * `messages/en.json`, or when a FR key lacks a complete `fr.meta.json`
 * entry. Run by `pnpm run check:i18n`, which is wired into `build` and
 * `test`. Runs on plain Node (>=22) via native TypeScript type stripping.
 */
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { findMissingKeys, findMissingMeta } from "../src/lib/i18n/check.ts";

const messagesDir = resolve(import.meta.dirname, "../messages");

function readJson(file: string): Record<string, unknown> {
  return JSON.parse(readFileSync(resolve(messagesDir, file), "utf8")) as Record<string, unknown>;
}

const fr = readJson("fr.json");
const en = readJson("en.json");
const meta = readJson("fr.meta.json");

const missingKeys = findMissingKeys(fr, en);
const missingMeta = findMissingMeta(fr, meta);

if (missingKeys.length > 0 || missingMeta.length > 0) {
  console.error("i18n check failed:");
  if (missingKeys.length > 0) {
    console.error(`  Missing EN translations (${missingKeys.length}):`);
    for (const key of missingKeys) console.error(`    - ${key}`);
  }
  if (missingMeta.length > 0) {
    console.error(`  Missing or incomplete fr.meta.json entries (${missingMeta.length}):`);
    for (const key of missingMeta) console.error(`    - ${key}`);
  }
  process.exit(1);
}

console.log(
  `i18n check passed: ${Object.keys(fr).length} FR keys all have EN translations and meta entries.`,
);
