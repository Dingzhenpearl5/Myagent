---
name: agent-memory-manager
description: This skill should be used when designing, debugging, or improving Agent conversation memory, including chat history persistence, session recovery, conversation titles, deletion, renaming, and privacy boundaries.
---

# Agent Memory Manager

Use this skill to improve memory and conversation-history behavior in chat Agent projects.

## Workflow

1. Inspect the state source of truth before editing: session state, local files, database, or remote storage.
2. Confirm when memory is loaded, updated, saved, and restored.
3. Verify new conversations, active conversation switching, and message appends stay in sync.
4. Add persistence only at stable boundaries such as create, append, rename, delete, or clear.
5. Validate that refresh/restart restores expected history without duplicating conversations.
6. Keep private conversation data out of git and logs.

## Checks

- Confirm the active conversation id points to an existing conversation.
- Confirm empty or corrupted memory files fail safely.
- Confirm titles update from the first user message when appropriate.
- Confirm user and assistant messages append to the selected conversation only.
- Confirm delete/clear behavior cannot accidentally remove unrelated project data.
- Confirm storage paths are ignored by git when they contain private chat content.

## Avoid

- Avoid logging full user messages by default.
- Avoid storing secrets or API keys in conversation memory.
- Avoid relying only on `st.session_state` when the requirement is persistence after refresh.
- Avoid broad migrations unless the current storage schema requires it.
