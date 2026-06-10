"""全局自定义 CSS 样式，实现 ChatGPT 风格布局。"""

CUSTOM_CSS = """
<style>
/* ========== 全局 ========== */
[data-testid="stAppViewContainer"] {
    background: #f7f7f8;
}

/* ========== 侧边栏 ========== */
[data-testid="stSidebar"] {
    background-color: #202123;
    min-width: 280px !important;
    max-width: 280px !important;
}
[data-testid="stSidebar"] * {
    color: #ececf1;
}
[data-testid="stSidebar"] hr {
    border-color: #4d4d4f;
}
[data-testid="stSidebar"] button {
    background-color: transparent !important;
    border: 1px solid #565869 !important;
    border-radius: 8px !important;
    color: #ececf1 !important;
    padding: 8px 16px !important;
    width: 100% !important;
}
[data-testid="stSidebar"] button:hover {
    background-color: #2b2c2e !important;
}
[data-testid="stSidebar"] button:focus {
    border-color: transparent !important;
    box-shadow: none !important;
}

/* 侧边栏 conversation 条目 */
.conv-item {
    display: flex;
    align-items: center;
    padding: 10px 12px;
    margin: 2px 8px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    color: #ececf1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    transition: background 0.15s;
}
.conv-item:hover {
    background-color: #2b2c2e;
}
.conv-item.active {
    background-color: #343541;
}

/* ========== 主区域 ========== */
.main > div {
    max-width: 100% !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

/* 标题栏 */
.chat-header {
    height: 56px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #e5e5e5;
    padding: 0 20px;
    font-size: 16px;
    font-weight: 600;
    color: #202123;
}

/* 消息区域 */
[data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

/* 空状态 */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 60vh;
    color: #8e8ea0;
    font-size: 18px;
    text-align: center;
}
.empty-state .icon {
    font-size: 48px;
    margin-bottom: 16px;
}

/* ========== 消息气泡 ========== */
.message-row {
    display: flex;
    padding: 12px 16px;
    gap: 12px;
}
.message-row.user {
    justify-content: flex-end;
}
.message-row.assistant {
    justify-content: flex-start;
}

.message-bubble {
    max-width: 70%;
    padding: 12px 16px;
    border-radius: 12px;
    font-size: 15px;
    line-height: 1.6;
    word-break: break-word;
}
.message-bubble.user-bubble {
    background-color: #2563eb;
    color: #ffffff;
    border-bottom-right-radius: 4px;
}
.message-bubble.assistant-bubble {
    background-color: #ffffff;
    color: #202123;
    border: 1px solid #e5e5e5;
    border-bottom-left-radius: 4px;
}

/* ========== 输入区 ========== */
[data-testid="stChatInput"] {
    background: #ffffff;
    border-top: 1px solid #e5e5e5;
    padding: 12px 20px;
}
[data-testid="stChatInput"] textarea {
    border-radius: 12px !important;
    border: 1px solid #d1d5db !important;
    padding: 10px 16px !important;
    font-size: 15px !important;
    min-height: 44px !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 2px rgba(37,99,235,0.1) !important;
}

/* ========== 隐藏不需要的元素 ========== */
#MainMenu, footer, header {
    visibility: hidden;
}
[data-testid="stSidebarNav"] {
    display: none;
}
[data-testid="stDecoration"] {
    display: none;
}
[data-testid="stStatusWidget"] {
    display: none;
}

/* 隐藏顶栏 */
.stApp header {
    background: transparent !important;
}
.stAppToolbar {
    display: none !important;
}

/* Spinner 样式优化 */
.stSpinner {
    text-align: center;
    padding: 20px;
    color: #8e8ea0;
}
</style>
"""
