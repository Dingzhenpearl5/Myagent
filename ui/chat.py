"""右侧聊天区域：标题栏 + 消息气泡 + 输入框。"""

import streamlit as st
from agent.agent_factory import invoke_agent
from ui.conversations import get_active_messages, append_message, get_active_title


def render_chat(agent) -> None:
    """渲染右侧聊天区域。

    包含三部分：
    1. 顶部标题栏
    2. 中间消息列表（气泡样式）
    3. 底部输入框

    Args:
        agent: 已初始化的 LangGraph ReAct Agent 实例
    """
    messages = get_active_messages()

    # --- 顶部：标题栏 ---
    title = get_active_title()
    st.markdown(
        f'<div class="chat-header">💬 {title}</div>',
        unsafe_allow_html=True,
    )

    # --- 中间：消息区域 ---
    if not messages:
        _render_empty_state()
    else:
        _render_messages(messages)

    # --- 底部：输入框 ---
    if prompt := st.chat_input("输入你的问题...", key="main_chat_input"):
        # 添加用户消息
        append_message("user", prompt)

        # 获取最新消息列表（含刚追加的）
        current_messages = get_active_messages()

        # 调用 Agent
        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
                try:
                    answer = invoke_agent(
                        agent=agent,
                        user_input=prompt,
                        history=current_messages[:-1],
                    )
                    append_message("assistant", answer)
                except Exception as e:
                    error_msg = f"抱歉，处理请求时出现错误: {str(e)}"
                    append_message("assistant", error_msg)

        st.rerun()


def _render_empty_state() -> None:
    """空对话时的占位提示。"""
    st.markdown(
        """
        <div class="empty-state">
            <div class="icon">🏢</div>
            <div>企业综合信息查询助手</div>
            <div style="font-size:14px;margin-top:8px;">
                试试问：北京天气怎么样？ ｜ 000001 股价多少？
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_messages(messages: list[dict]) -> None:
    """用自定义 HTML 气泡渲染消息列表。

    Args:
        messages: 消息列表 [{"role": "user"/"assistant", "content": "..."}]
    """
    for msg in messages:
        role = msg["role"]
        content = msg["content"].replace("\n", "<br>")
        is_user = role == "user"

        row_class = "message-row user" if is_user else "message-row assistant"
        bubble_class = "user-bubble" if is_user else "assistant-bubble"
        avatar = "👤" if is_user else "🤖"

        html = f"""
        <div class="{row_class}">
            <div class="message-bubble {bubble_class}">
                {content}
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
