import streamlit as st
from config.settings import DEEPSEEK_API_KEY
from agent.agent_factory import create_agent
from ui.sidebar import render_sidebar
from ui.chat import render_chat

# 页面配置
st.set_page_config(
    page_title="企业综合信息查询助手",
    page_icon="🏢",
    layout="wide",
)

st.title("🏢 企业综合信息查询助手")

# 侧边栏
render_sidebar()

# 初始化 Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = None

# 初始化 Agent
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

# 对话区域
render_chat(st.session_state.agent)
