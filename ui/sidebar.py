import streamlit as st
from config.settings import DEEPSEEK_API_KEY, AMAP_API_KEY


def render_sidebar() -> None:
    """渲染侧边栏：展示 API Key 配置状态。"""
    st.sidebar.title("🔧 配置状态")

    # DeepSeek API Key 状态
    if DEEPSEEK_API_KEY:
        st.sidebar.success("✅ DeepSeek API Key 已配置")
    else:
        st.sidebar.error("❌ DeepSeek API Key 未配置")
        st.sidebar.info("请在 .env 文件中设置 DEEPSEEK_API_KEY")

    # 高德 API Key 状态
    if AMAP_API_KEY:
        st.sidebar.success("✅ 高德 API Key 已配置")
    else:
        st.sidebar.error("❌ 高德 API Key 未配置")
        st.sidebar.info("请在 .env 文件中设置 AMAP_API_KEY")

    st.sidebar.divider()

    # 可用工具说明
    st.sidebar.subheader("可用工具")
    st.sidebar.markdown(
        """
        - 🌤️ **天气查询** — 查询城市实时天气
        - 📈 **股票查询** — 查询 A 股实时行情
        - 📄 **内部资料** — 公司文档查询（开发中）
        """
    )

    st.sidebar.divider()

    # 使用提示
    st.sidebar.subheader("使用提示")
    st.sidebar.markdown(
        """
        试试这些问题：
        - "北京今天天气怎么样？"
        - "000001 股价多少？"
        - "茅台涨了吗？"
        """
    )
