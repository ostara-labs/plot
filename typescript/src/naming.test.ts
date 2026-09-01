/**
 * Naming guard: reject vague variable names in the source tree (27.27).
 *
 * Biome `namingConvention` enforces casing; this test enforces the semantic
 * half of the convention — identifiers must reveal intent. Extend the banned
 * list rather than adding ignores.
 */
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";

const SRC_DIR = join(import.meta.dirname, "..", "src");

const BANNED_NAMES = new Set([
  "data",
  "tmp",
  "temp",
  "res",
  "obj",
  "foo",
  "bar",
  "baz",
  "stuff",
  "thing",
  "val",
  "vals",
]);

// `const name =`, `let name =`, `function name(`, `for (const name of/in`
const DECLARATION = new RegExp(
  `\\b(?:const|let|var|function|for\\s*\\(\\s*(?:const|let|var)\\s+)(${[...BANNED_NAMES].join("|")})\\b`,
);

function* walk(dir: string): Generator<string> {
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) {
      if (entry === "paraglide") continue; // generated output
      yield* walk(full);
    } else if (/\.(ts|js)$/.test(entry)) {
      yield full;
    }
  }
}

describe("naming guard (27.27)", () => {
  it("has no vague variable names in src", () => {
    const offenders: string[] = [];
    for (const file of walk(SRC_DIR)) {
      const lines = readFileSync(file, "utf8").split("\n");
      lines.forEach((line, index) => {
        const match = DECLARATION.exec(line);
        if (match) {
          offenders.push(`${file.replace(SRC_DIR, "src")}:${index + 1}: ${match[1]}`);
        }
      });
    }
    expect(offenders).toEqual([]);
  });
});
