/** Unique-identifier suggestion: slug from a display name (ADR/UI contract). */
export function slugify(value: string): string {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
}

/**
 * Attach auto-suggestion to an AntD form: when `sourceField` changes and the
 * user has NOT manually edited `targetField` (tracked via a hidden marker),
 * fill `targetField` with the slugified source value.
 */
export function trackCodeSuggestion(
  form: { getFieldValue: (name: string | string[]) => unknown; setFieldValue: (name: string | string[], value: unknown) => void },
  sourceField: string,
  targetField: string,
  changed: { name: string | number | (string | number)[] },
  values: Record<string, unknown>,
): void {
  const name = changed.name;
  if (name === sourceField && typeof values[sourceField] === "string") {
    form.setFieldValue(targetField, slugify(values[sourceField] as string));
  }
}
