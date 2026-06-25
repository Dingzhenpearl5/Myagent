---
name: api-integration-checker
description: This skill should be used when validating or debugging third-party API integrations, including API keys, request parameters, endpoint URLs, response codes, retries, and user-facing error messages.
---

# API Integration Checker

Use this skill to verify external API integrations used by Agent tools and services.

## Workflow

1. Inspect the service module and configuration source before editing.
2. Compare endpoint URL, method, required parameters, and optional parameters against the provider documentation.
3. Check API key presence, platform permissions, quota, and known error codes.
4. Run the smallest direct service function test when possible.
5. Improve error handling so the user sees the real actionable cause.
6. Add local fallback mappings only when they are stable and low-risk.

## Checks

- Confirm required environment variables are loaded from settings.
- Confirm request timeout is set.
- Confirm JSON parsing handles missing or malformed fields.
- Confirm provider error codes are mapped to readable messages.
- Confirm no secrets are printed or committed.

## Avoid

- Avoid assuming a network/API failure is an Agent failure.
- Avoid hardcoding secrets.
- Avoid masking permission errors as generic temporary failures.
