---
name: write-typescript
user-invocable: false
description: TypeScript rules for types, narrowing, validation at boundaries, and tests. Use when reading or editing any .ts or .tsx file.
paths: ["**/*.ts", "**/*.tsx"]
metadata:
  based-on: "typescript-best-practices, principle-type-system-discipline and principle-boundary-discipline from pstack by Lauren Tan, via michael-denyer/pstack-claude (MIT)"
---

# TypeScript best practices

Make the compiler reject impossible states, mismatched primitives, and unhandled variants. Prefer defining errors and special cases out of existence over adding handlers for them.

| Rule | Summary |
|------|---------|
| Discriminated unions | Model variants with a `kind` literal discriminant so impossible states can't be represented. No optional-field bags. |
| Branded types | Brand primitives with `& { readonly __brand: "X" }` so they can't be mixed up. If two arguments share a primitive type but mean different things, brand them. Validate once at the boundary. |
| Constructive modeling | Build the shape so the illegal value can't be constructed. `[T, ...T[]]` for non-empty, `[T, T][]` for even length, `start` plus `duration` for a range. Not a runtime guard, not a wish for refinement types. |
| Simplest total type | Keep `T[]` while every operation on it stays total. Strengthen to `NonEmpty<T>` only where the loose type forces `!`, a cast, or a "should never happen" throw. |
| `unknown` over `any` | External data is `unknown`. |
| Schemas before guards | Before hand-writing a property-by-property type guard, use the repository's runtime schema library and infer the type from the schema, such as `z.infer`. |
| No `as` casts | Every `as` is a runtime crash waiting. Cast only after validation. |
| Narrowing hierarchy | Discriminant switch > `in` operator > `typeof`/`instanceof` > user-defined type guard > `as`. |
| Type guards | Must verify the claim. A lying guard is worse than `as` because the bug hides behind a name that says it's safe. Name them `isX` or `hasX`. |
| Exhaustiveness | Inline `const _exhaustive: never = x;` in default arms so the compiler errors when a new variant is added. |
| `satisfies` over `as` | Validates the value without widening literal types. |
| Boundary validation | Parse where data crosses in, into a named domain type. `Record<string, unknown>` (however spelled) stops at that parse. Trust types inside. See **Boundaries** below. |
| Schema-derived types | When a proto, OpenAPI spec, GraphQL schema, migration, or other file owns a shape, derive from it. Reach for `Pick`/`Omit`/`Parameters`/`ReturnType`/`Awaited`/`typeof` before declaring a new interface. |
| Object args | Pass objects, not positional, so argument order is self-documenting. Skip on hot paths (per-frame render, tokenizers, parsers). |
| Real tests | Don't mock what you can run. Prefer the framework's real test primitives with leak/disposable checks, and verify UI in a running build. Mock only what you can't run locally. |
| Structured telemetry | Prefer structured logger diagnostics with enough context to debug from an id. No `console.log` in shipped code. |

Examples: `references/patterns.md`.

## Boundaries

Put validation, type narrowing, and error handling at system boundaries. Trust internal code. Business logic lives in pure functions; the shell around it is thin and mechanical. Scattered validation is noisy, redundant, and gives a false sense of safety.

- **At boundaries** (CLI args, config files, environment variables, external APIs, RPC payloads, `JSON.parse`, IPC, database rows): parse into the typed model, return errors, handle defensively.
- **Inside the system:** typed data, error propagation, no re-validation, no redundant null checks deep in call chains.
- **Across the boundary:** expose domain concepts, not transport, storage, framework, or wire types.
- **The tests:** "Is this data crossing a system boundary right now?" If not, validation is redundant. "Can this be a pure function the shell just calls?" If yes, extract it.
