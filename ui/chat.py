"""右侧聊天区域：GPT 风格标题栏 + 纯文本消息流 + 输入框。"""

from html import escape

import streamlit as st
from agent.agent_factory import invoke_agent
from ui.conversations import get_active_messages, append_message, get_active_title


def render_chat(agent) -> None:
    """渲染右侧聊天区域。"""
    messages = get_active_messages()
    title = escape(get_active_title())

    st.markdown(
        f"""
        <div class="chat-shell">
            <div class="chat-topbar">
                <div class="chat-title">{title}</div>
            </div>
            <div class="chat-content">
        """,
        unsafe_allow_html=True,
    )

    if not messages:
        _render_empty_state()
    else:
        _render_messages(messages)

    st.markdown("</div></div>", unsafe_allow_html=True)

    if prompt := st.chat_input("给助手发送消息", key="main_chat_input"):
        append_message("user", prompt)
        current_messages = get_active_messages()

        try:
            with st.spinner("正在思考..."):
                answer = invoke_agent(
                    agent=agent,
                    user_input=prompt,
                    history=current_messages[:-1],
                )
            append_message("assistant", answer)
        except Exception as e:
            append_message("assistant", f"抱歉，处理请求时出现错误：{str(e)}")

        st.rerun()


def _render_empty_state() -> None:
    """空对话时的占位提示。"""
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-title">今天想查询什么？</div>
            <div class="empty-subtitle">可以查询内部制度、天气、股票，也可以继续普通对话。</div>
            <div class="prompt-grid">
                <div class="prompt-card">怎么打卡？</div>
                <div class="prompt-card">报销多久到账？</div>
                <div class="prompt-card">可以使用 AI 工具处理客户资料吗？</div>
                <div class="prompt-card">查询 000001 当前股价</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_messages(messages: list[dict]) -> None:
    """使用纯文本消息块渲染消息。"""
    for msg in messages:
        role = msg.get("role", "assistant")
        role_label = "你" if role == "user" else "助手"
        content = escape(msg.get("content", "")).replace("\n", "<br>")
        message_class = "user-message" if role == "user" else "assistant-message"

        st.markdown(
            f"""
            <div class="plain-message {message_class}">
                <div class="message-label">{role_label}</div>
                <div class="message-content">{content}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
