---
name: agent-observability
description: This skill should be used when adding lightweight observability to an Agent app, including tool-call traces, request timing, service errors, debug logs, and readable diagnostics without exposing secrets.
---

# Agent Observability

Use this skill to add practical debugging visibility to Agent applications.

## Workflow

1. Identify the smallest place to observe the behavior: Agent invocation, tool wrapper, or service boundary.
2. Add structured, minimal logs that help diagnose tool selection and failures.
3. Include timing only when performance or latency is relevant.
4. Redact secrets, tokens, keys, and private user data.
5. Keep logs optional or low-noise for normal app usage.
6. Surface user-facing diagnostics only when they help the user take action.

## Useful Signals

- User query category.
- Selected tool name.
- Tool input arguments after normalization.
- Service endpoint category, not full secret-bearing URL.
- Provider error code and mapped message.
- Elapsed time for slow services.

## Avoid

- Avoid printing API keys or full authenticated URLs.
- Avoid logging entire conversation history by default.
- Avoid noisy logs that obscure actual failures.
