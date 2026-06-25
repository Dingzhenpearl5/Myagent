"""本地对话记忆存储。"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

STORE_PATH = Path(__file__).resolve().parents[1] / "data" / "conversations.json"


def load_conversations() -> list[dict]:
    """从本地 JSON 文件读取对话列表。"""
    if not STORE_PATH.exists():
        return []

    try:
        data = json.loads(STORE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        logger.exception("conversation store load failed")
        return []

    if not isinstance(data, list):
        return []

    conversations = []
    for item in data:
        if not isinstance(item, dict):
            continue
        conv_id = item.get("id")
        title = item.get("title") or "新对话"
        messages = item.get("messages")
        if not isinstance(conv_id, str) or not isinstance(messages, list):
            continue
        conversations.append({"id": conv_id, "title": str(title), "messages": messages})
    return conversations


def save_conversations(conversations: list[dict]) -> None:
    """将对话列表保存到本地 JSON 文件。"""
    try:
        STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
        STORE_PATH.write_text(
            json.dumps(conversations, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except OSError:
        logger.exception("conversation store save failed")
