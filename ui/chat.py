import streamlit as st
from agent.agent_factory import invoke_agent


def render_chat(agent) -> None:
    """渲染对话区域并处理用户消息。

    读取 session_state 中的对话历史，展示所有消息，
    处理用户新输入，调用 Agent 并追加结果到历史。

    Args:
        agent: 已初始化的 LangGraph ReAct Agent 实例
    """
    # 显示历史消息
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 用户输入
    if prompt := st.chat_input("输入你的问题..."):
        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 调用 Agent
        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
                try:
                    answer = invoke_agent(
                        agent=agent,
                        user_input=prompt,
                        history=st.session_state.messages[:-1],
                    )
                    st.markdown(answer)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )
                except Exception as e:
                    error_msg = f"抱歉，处理请求时出现错误: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg}
                    )
