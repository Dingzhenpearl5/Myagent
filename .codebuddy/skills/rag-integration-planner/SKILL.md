---
name: rag-integration-planner
description: This skill should be used when planning or implementing RAG/internal document search for an Agent, including document loading, chunking, embeddings, retrieval, citations, and fallback behavior.
---

# RAG Integration Planner

Use this skill when adding internal document search or knowledge-base retrieval to an Agent.

## Workflow

1. Inspect the existing placeholder tool and service boundaries before editing.
2. Define the document sources, update frequency, and privacy constraints.
3. Choose a minimal retrieval path: load documents, split chunks, embed, store, retrieve, format answer.
4. Keep the Agent tool contract stable and return concise, grounded results.
5. Add clear fallback messages when the knowledge base is empty or retrieval fails.
6. Add focused tests for chunk formatting, empty results, and tool output.

## Checks

- Confirm retrieved content is relevant to the user query.
- Confirm answers do not invent document facts when retrieval is empty.
- Confirm citations or source names are included when available.
- Confirm sensitive internal data is not logged.
- Confirm index files or document caches are ignored by git if they contain private content.
- Confirm RAG failures are surfaced as readable assistant messages.

## Avoid

- Avoid wiring a vector database before the local MVP path is clear.
- Avoid returning large raw document chunks directly to the user.
- Avoid mixing unrelated web search results into internal document answers.
- Avoid changing model prompts and retrieval logic in one large refactor unless necessary.
