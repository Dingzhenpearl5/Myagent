---
name: agent-tool-debugger
description: This skill should be used when debugging an Agent's tool-calling behavior, including whether tools are selected, invoked with correct arguments, passed conversation history, and surfaced clearly in responses.
---

# Agent Tool Debugger

Use this skill to inspect and fix tool-calling behavior in Python chat Agent projects.

## Workflow

1. Inspect the Agent factory, tool registration, and invocation path.
2. Identify available tools and their expected input/output format.
3. Trace how user input and chat history are passed into the Agent.
4. Verify whether the Agent should call a tool or answer directly.
5. Add minimal logging or readable errors only when useful for debugging.
6. Validate the target query through the narrowest relevant function or service test.

## Checks

- Confirm tools are registered with clear names and descriptions.
- Confirm tool functions return concise, user-readable results.
- Confirm exceptions are caught at service boundaries and not silently swallowed.
- Confirm chat history excludes the newly appended user message when passed as prior history.
- Confirm failed tool calls produce actionable assistant messages.

## Avoid

- Avoid changing model prompts and service code at the same time unless necessary.
- Avoid broad refactors while debugging one tool.
- Avoid hiding raw API errors before they are mapped to useful user-facing messages.
