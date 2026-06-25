"""左侧边栏：对话列表管理。"""

import streamlit as st
import uuid
from config.settings import DEEPSEEK_API_KEY, AMAP_API_KEY
from ui.conversation_store import load_conversations, save_conversations


def _get_active_index() -> int | None:
    """获取当前激活对话在列表中的索引。"""
    convs = st.session_state.conversations
    active_id = st.session_state.active_conversation_id
    if active_id is None or not convs:
        return None
    for i, c in enumerate(convs):
        if c["id"] == active_id:
            return i
    return None


def _get_active_conversation() -> dict | None:
    """获取当前激活的对话对象。"""
    idx = _get_active_index()
    if idx is not None:
        return st.session_state.conversations[idx]
    return None


def _set_active(conv_id: str) -> None:
    """切换激活的对话。"""
    st.session_state.active_conversation_id = conv_id


def _new_conversation() -> None:
    """创建新对话。"""
    new_id = str(uuid.uuid4())
    st.session_state.conversations.insert(
        0,
        {"id": new_id, "title": "新对话", "messages": []},
    )
    st.session_state.active_conversation_id = new_id
    save_conversations(st.session_state.conversations)


def _build_history_entries(conversations: list[dict]) -> list[dict]:
    """按用户提问构建侧栏历史记录。"""
    entries = []
    for conv in conversations:
        user_messages = [msg for msg in conv.get("messages", []) if msg.get("role") == "user"]
        if not user_messages:
            entries.append(
                {
                    "conversation_id": conv["id"],
                    "title": conv.get("title") or "新对话",
                    "message_index": 0,
                }
            )
            continue

        for message_index, message in enumerate(user_messages, start=1):
            content = (message.get("content") or "").strip()
            entries.append(
                {
                    "conversation_id": conv["id"],
                    "title": content or conv.get("title") or "新对话",
                    "message_index": message_index,
                }
            )
    return entries


def render_conversations() -> None:
    """渲染侧边栏：新建对话按钮 + 对话列表 + 底部设置。

    同时返回当前对话的 messages 引用，方便 chat.py 使用。
    """
    # --- 初始化 session_state ---
    if "conversations" not in st.session_state:
        st.session_state.conversations = load_conversations()
    if "active_conversation_id" not in st.session_state:
        st.session_state.active_conversation_id = None

    active_id = st.session_state.active_conversation_id
    existing_ids = {conv["id"] for conv in st.session_state.conversations}
    if active_id not in existing_ids:
        st.session_state.active_conversation_id = (
            st.session_state.conversations[0]["id"] if st.session_state.conversations else None
        )

    # 如果没有任何对话，自动创建一个
    if not st.session_state.conversations:
        _new_conversation()

    # --- 顶部：新建对话按钮 ---
    st.sidebar.markdown(
        '<div class="sidebar-title">AI 助手</div>',
        unsafe_allow_html=True,
    )
    if st.sidebar.button("新建聊天", use_container_width=True):
        _new_conversation()
        st.rerun()

    st.sidebar.markdown(
        '<div class="history-title">历史记录</div>',
        unsafe_allow_html=True,
    )

    # --- 中间：对话列表 ---
    conversations = st.session_state.conversations
    active_id = st.session_state.active_conversation_id

    # 使用按钮渲染历史记录，每条用户提问可点击切换回所属对话
    history_entries = _build_history_entries(conversations)
    if not history_entries:
        st.sidebar.caption("暂无历史记录")

    for entry in history_entries:
        is_active = entry["conversation_id"] == active_id
        title = entry["title"] or "新对话"
        display_title = title[:20] + "…" if len(title) > 20 else title
        if st.sidebar.button(
            display_title,
            key=f"history_btn_{entry['conversation_id']}_{entry['message_index']}",
            use_container_width=True,
            disabled=is_active and entry["message_index"] == 0,
        ):
            _set_active(entry["conversation_id"])
            st.rerun()

    # --- 底部：设置（折叠） ---
    st.sidebar.divider()
    with st.sidebar.expander("设置", expanded=False):
        if DEEPSEEK_API_KEY:
            st.sidebar.success("DeepSeek API Key 已配置")
        else:
            st.sidebar.error("DeepSeek API Key 未配置")

        if AMAP_API_KEY:
            st.sidebar.success("高德 API Key 已配置")
        else:
            st.sidebar.error("高德 API Key 未配置")

        st.sidebar.caption("可用工具：天气 / 股票 / 内部资料")


def get_active_messages() -> list[dict]:
    """获取当前对话的 messages 列表引用。"""
    conv = _get_active_conversation()
    if conv is None:
        return []
    return conv["messages"]


def get_active_title() -> str:
    """获取当前对话标题。"""
    conv = _get_active_conversation()
    if conv is None:
        return "企业综合信息查询助手"
    return conv["title"] or "新对话"


def append_message(role: str, content: str) -> None:
    """向当前对话追加一条消息。"""
    conv = _get_active_conversation()
    if conv is None:
        return
    conv["messages"].append({"role": role, "content": content})

    # 自动生成标题：第一条用户消息的前 20 个字符
    if (
        role == "user"
        and len(conv["messages"]) == 1
        and (conv["title"] == "新对话" or not conv["title"])
    ):
        title = content.strip()
        if len(title) > 20:
            title = title[:20] + "…"
        conv["title"] = title

    save_conversations(st.session_state.conversations)
