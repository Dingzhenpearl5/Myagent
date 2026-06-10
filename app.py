"""
企业综合信息查询 Agent — Streamlit 入口
布局：左侧对话列表（深色） + 右侧聊天区（浅色）
"""

import streamlit as st

from config.settings import DEEPSEEK_API_KEY
from agent.agent_factory import create_agent
from ui.styles import CUSTOM_CSS
from ui.conversations import render_conversations
from ui.chat import render_chat

# ── 页面配置 ──
st.set_page_config(
    page_title="企业综合信息查询助手",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="auto",
)

# ── 注入全局样式 ──
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── 左侧：对话列表 ──
render_conversations()

# ── 初始化 Agent（只创建一次，缓存在 session_state） ──
if "agent" not in st.session_state:
    st.session_state.agent = None

if st.session_state.agent is None:
    if not DEEPSEEK_API_KEY:
        st.warning("⚠️ 请先在 .env 文件中配置 DEEPSEEK_API_KEY，然后刷新页面。")
        st.stop()
    try:
        with st.spinner("正在初始化 Agent..."):
            st.session_state.agent = create_agent()
    except Exception as e:
        st.error(f"Agent 初始化失败: {str(e)}")
        st.stop()

# ── 右侧：聊天区域 ──
render_chat(st.session_state.agent)
