/**
 * i18n completeness checks (spec wave-01, decision 27.17).
 *
 * FR is the source of truth (`messages/fr.json`). Every FR key must have an
 * EN translation (`messages/en.json`) and a meta entry (`messages/fr.meta.json`)
 * with `context` and `usage` (spec wave-01 §3). The build and the test suite
 * both fail when a key is missing — forcing translation completeness before
 * deploy.
 */

export type MessageFile = Record<string, unknown>;

/**
 * Flatten a message file into a flat `key -> string` map. Handles both flat
 * snake_case keys (`project.new_button`) and nested objects. The `$schema`
 * key is metadata and is ignored.
 */
export function flattenMessages(messageNode: MessageFile, prefix = ""): Record<string, string> {
  const result: Record<string, string> = {};
  for (const [key, value] of Object.entries(messageNode)) {
    if (key === "$schema") continue;
    const fullKey = prefix ? `${prefix}.${key}` : key;
    if (typeof value === "string") {
      result[fullKey] = value;
    } else if (value !== null && typeof value === "object") {
      Object.assign(result, flattenMessages(value as MessageFile, fullKey));
    }
  }
  return result;
}

/**
 * Keys present in FR but missing from EN. Empty when complete (27.17).
 */
export function findMissingKeys(fr: MessageFile, en: MessageFile): string[] {
  const frFlat = flattenMessages(fr);
  const enFlat = flattenMessages(en);
  return Object.keys(frFlat).filter((key) => !(key in enFlat));
}

/**
 * FR keys whose `fr.meta.json` entry is missing or lacks the mandatory
 * `context` and `usage` fields (spec wave-01 §3).
 */
export function findMissingMeta(fr: MessageFile, meta: MessageFile): string[] {
  const frFlat = flattenMessages(fr);
  return Object.keys(frFlat).filter((key) => {
    const entry = meta[key];
    if (entry === null || typeof entry !== "object") return true;
    const fields = entry as Record<string, unknown>;
    return (
      typeof fields.context !== "string" ||
      fields.context.length === 0 ||
      typeof fields.usage !== "string" ||
      fields.usage.length === 0
    );
  });
}
