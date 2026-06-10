"""左侧边栏：对话列表管理。"""

import streamlit as st
import uuid
from config.settings import DEEPSEEK_API_KEY, AMAP_API_KEY


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


def render_conversations() -> None:
    """渲染侧边栏：新建对话按钮 + 对话列表 + 底部设置。

    同时返回当前对话的 messages 引用，方便 chat.py 使用。
    """
    # --- 初始化 session_state ---
    if "conversations" not in st.session_state:
        st.session_state.conversations = []
    if "active_conversation_id" not in st.session_state:
        st.session_state.active_conversation_id = None

    # 如果没有任何对话，自动创建一个
    if not st.session_state.conversations:
        _new_conversation()

    # --- 顶部：新建对话按钮 ---
    with st.sidebar.container():
        if st.sidebar.button("+ 新建对话", use_container_width=True):
            _new_conversation()
            st.rerun()

    st.sidebar.divider()

    # --- 中间：对话列表 ---
    conversations = st.session_state.conversations
    active_id = st.session_state.active_conversation_id

    # 使用自定义 HTML 渲染对话列表（支持高亮和省略号）
    items_html = ""
    for i, conv in enumerate(conversations):
        is_active = conv["id"] == active_id
        css_class = "conv-item active" if is_active else "conv-item"
        title = conv["title"] or "新对话"
        # 给每个对话一个可点击的标记
        items_html += f"""<div class="{css_class}" id="conv-{i}">💬 {title}</div>"""

    st.sidebar.markdown(items_html, unsafe_allow_html=True)

    # 用 selectbox（隐形）实现点击切换
    # Streamlit 没有直接的点击事件，用 radio/selectbox 模拟
    if len(conversations) > 1:
        titles = [c["title"] or f"对话 {i+1}" for i, c in enumerate(conversations)]
        selected = st.sidebar.radio(
            "对话列表",
            options=list(range(len(conversations))),
            format_func=lambda i: titles[i],
            index=_get_active_index() or 0,
            key="conv_radio",
            label_visibility="collapsed",
        )
        if conversations[selected]["id"] != active_id:
            _set_active(conversations[selected]["id"])
            st.rerun()

    # --- 底部：设置（折叠） ---
    st.sidebar.divider()
    with st.sidebar.expander("⚙️ 设置", expanded=False):
        if DEEPSEEK_API_KEY:
            st.sidebar.success("✅ DeepSeek API Key 已配置")
        else:
            st.sidebar.error("❌ DeepSeek API Key 未配置")

        if AMAP_API_KEY:
            st.sidebar.success("✅ 高德 API Key 已配置")
        else:
            st.sidebar.error("❌ 高德 API Key 未配置")

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
