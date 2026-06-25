---
name: python-service-tester
description: This skill should be used when adding or repairing focused Python tests for Agent services, tools, and utility modules, especially API wrappers, data formatting, and fallback behavior.
---

# Python Service Tester

Use this skill to add focused tests for Python service modules used by Agent tools.

## Workflow

1. Inspect existing tests and adjacent service modules.
2. Identify the smallest behavior worth testing.
3. Prefer unit tests for parsing, formatting, fallback, and error mapping.
4. Mock external network calls instead of relying on live APIs.
5. Run the narrowest relevant test command first.
6. Avoid changing production code only to satisfy a weak test.

## Test Targets

- API response parsing.
- Error-code mapping.
- City/code normalization.
- Stock code normalization.
- Cache behavior where deterministic.
- Tool output formatting.

## Avoid

- Avoid adding tests to projects with no test pattern unless requested.
- Avoid live API calls in automated tests.
- Avoid broad test rewrites unrelated to the target bug.
