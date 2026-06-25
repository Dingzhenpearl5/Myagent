---
name: streamlit-agent-ux
description: This skill should be used when improving, reviewing, or debugging the Streamlit chat Agent user experience, including sidebar chat history, selected conversation rendering, input panel styling, spacing, layout alignment, and Streamlit CSS overrides.
---

# Streamlit Agent UX

Use this skill to improve Streamlit chat Agent interfaces that use a fixed conversation-history sidebar and a main selected-conversation chat area.

## Core Goals

- Preserve a stable two-pane layout: fixed left history list, main right chat view.
- Keep the input panel as the primary visual focus.
- Avoid excessive decorative UI around the chat content.
- Prefer simple, predictable spacing over large blank regions.
- Avoid emojis, avatar images, or icon-heavy UI unless explicitly requested.
- Preserve reliable Streamlit behavior over fragile custom JavaScript.

## Project Patterns

- Treat `app.py` as the entrypoint and avoid moving layout orchestration out of it unnecessarily.
- Treat `ui/conversations.py` as the source of truth for conversation state and sidebar history.
- Treat `ui/chat.py` as the selected conversation renderer and input handler.
- Treat `ui/styles.py` as the single place for global CSS overrides.
- Keep `st.sidebar` fixed and expanded for this project; do not reintroduce sidebar collapse behavior.

## UI Review Workflow

1. Inspect `ui/styles.py`, `ui/chat.py`, and `ui/conversations.py` before editing.
2. Identify whether the issue comes from Streamlit layout, custom HTML structure, or CSS overrides.
3. Fix root layout issues before adding more CSS selectors.
4. Prefer small targeted CSS changes over rewriting the full stylesheet.
5. Validate that the selected conversation still renders from `active_conversation_id`.
6. Check linter diagnostics for touched files.

## Styling Rules

- Keep the left sidebar visually separated from the chat area with a clear vertical border or subtle shadow.
- Keep the sidebar light themed unless the user explicitly asks for dark mode.
- Add a `历史记录` title above the history list and use a divider/underline to distinguish it from the list.
- Style conversation history entries as readable text cards with a clear selected state.
- Keep the main chat area mostly white and uncluttered.
- Use the bottom input panel as the strongest visual element through border, radius, and shadow.
- Avoid making the whole chat area a large floating card if it causes title/content misalignment.
- Avoid large `min-height`, excessive top padding, or centered empty states that create scrollable blank space.
- Use `html.escape` before rendering user or assistant content through `unsafe_allow_html=True`.

## Common Streamlit Pitfalls

- Avoid hiding `header[data-testid="stHeader"]` in a way that breaks layout controls unless sidebar collapse is intentionally disabled.
- Avoid relying on unstable `data-testid` selectors more than necessary.
- Avoid broad selectors such as `[data-testid="stChatInput"] div` when they override nested button or textarea styles unexpectedly.
- Avoid custom JavaScript click handlers for sidebar toggling.
- Avoid `st.chat_message` when the requirement is no avatars or images; use escaped custom HTML text blocks instead.

## Spacing Checklist

- Verify the gap between the conversation title and empty-state prompt is small.
- Verify the gap between messages and the input panel is not excessive.
- Verify the input panel does not create a dark or oversized bottom block.
- Verify no large card wrapper pushes the homepage prompt downward.
- Verify responsive widths remain aligned between title, content, spinner, and input panel.

## Agent UX Checklist

- Confirm clicking a history item updates `active_conversation_id` and reruns the app.
- Confirm the active conversation is visually distinct.
- Confirm creating a new chat inserts it at the top and selects it.
- Confirm user messages and assistant messages append to the selected conversation only.
- Confirm tool/API errors appear as readable assistant messages.
