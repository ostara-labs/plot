/**
 * Naming guard: reject vague variable names in the source tree (27.27).
 *
 * Biome `useNamingConvention` enforces casing; this test enforces the
 * semantic half of the convention — declared bindings must reveal intent.
 * Uses the TypeScript compiler for syntax-aware traversal so parameters,
 * destructuring and multi-declarators are all covered; Svelte `<script>`
 * blocks are parsed too. Property names (obj.data, { data: 1 }) are not
 * bindings and are exempt. Extend the banned list rather than adding
 * ignores.
 */
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";
import ts from "typescript";
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

interface Offender {
  file: string;
  line: number;
  name: string;
}

function* walk(dir: string): Generator<string> {
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) {
      if (entry === "paraglide") continue; // generated output
      yield* walk(full);
    } else if (/\.(ts|js|svelte)$/.test(entry)) {
      yield full;
    }
  }
}

/**
 * True when the identifier names a property rather than a binding: member
 * access (`response.data`), qualified types, or object literal keys.
 */
function isPropertyPosition(node: ts.Identifier): boolean {
  const { parent } = node;
  if (ts.isPropertyAccessExpression(parent) && parent.name === node) {
    return true;
  }
  if (ts.isQualifiedName(parent) && parent.right === node) {
    return true;
  }
  if ((ts.isPropertyAssignment(parent) || ts.isMethodDeclaration(parent)) && parent.name === node) {
    return true;
  }
  return false;
}

function scanSource(
  file: string,
  sourceText: string,
  lineOffset: number,
  offenders: Offender[],
): void {
  const source = ts.createSourceFile(file, sourceText, ts.ScriptTarget.Latest, true);
  const visit = (node: ts.Node): void => {
    if (ts.isIdentifier(node) && BANNED_NAMES.has(node.text) && !isPropertyPosition(node)) {
      const { line } = source.getLineAndCharacterOfPosition(node.getStart());
      offenders.push({ file, line: line + 1 + lineOffset, name: node.text });
    }
    node.forEachChild(visit);
  };
  source.forEachChild(visit);
}

describe("naming guard (27.27)", () => {
  it("has no vague bindings in src (ts, js, svelte scripts)", () => {
    const offenders: Offender[] = [];
    for (const file of walk(SRC_DIR)) {
      const content = readFileSync(file, "utf8");
      if (file.endsWith(".svelte")) {
        for (const match of content.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)) {
          const lineOffset = content.slice(0, match.index).split("\n").length - 1;
          scanSource(file, match[1], lineOffset, offenders);
        }
      } else {
        scanSource(file, content, 0, offenders);
      }
    }
    const messages = offenders.map((o) => `${o.file.replace(SRC_DIR, "src")}:${o.line}: ${o.name}`);
    expect(messages).toEqual([]);
  });
});
