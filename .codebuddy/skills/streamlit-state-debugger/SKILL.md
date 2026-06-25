---
name: streamlit-state-debugger
description: This skill should be used when debugging Streamlit session state, reruns, buttons, chat input, selected conversation state, and UI updates after user interactions.
---

# Streamlit State Debugger

Use this skill to diagnose Streamlit state and rerun issues in chat applications.

## Workflow

1. Inspect initialization order in the entrypoint and UI modules.
2. Identify the source of truth for each state key.
3. Verify widgets use stable keys and do not conflict across reruns.
4. Check whether callbacks update state before or after rendering dependent UI.
5. Use `st.rerun()` only after state changes that must immediately redraw the page.
6. Validate state transitions for new chat, select chat, submit message, and refresh.

## Checks

- Confirm `st.session_state` keys are initialized before use.
- Confirm active ids remain valid after loading, deleting, or creating records.
- Confirm button disabled states do not hide the current selection from the user.
- Confirm chat input submission appends messages before triggering rerun.
- Confirm expensive objects such as Agent instances are cached or initialized once.
- Confirm CSS overrides are not mistaken for state bugs.

## Avoid

- Avoid mutating widget-owned keys directly unless necessary.
- Avoid multiple reruns for one user action.
- Avoid generating random widget keys on every render.
- Avoid using custom JavaScript for normal Streamlit state updates.
