"""全局自定义 CSS：稳定的 ChatGPT 风格浅色聊天界面。"""

CUSTOM_CSS = """
<style>
:root {
    --bg: #ffffff;
    --surface: #f7f7f8;
    --surface-hover: #ececf1;
    --border: #e5e5e5;
    --text: #0f0f0f;
    --muted: #6b7280;
    --sidebar: #f7f8fa;
    --sidebar-hover: #eef2ff;
    --sidebar-active: #ffffff;
    --sidebar-border: #e5e7eb;
    --accent: #2563eb;
}

* {
    box-sizing: border-box;
}

.stApp {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

.main .block-container {
    max-width: 100% !important;
    padding: 0 !important;
}

#MainMenu,
footer,
.stAppToolbar,
[data-testid="stDecoration"] {
    display: none !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
}

[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] {
    display: none !important;
}

/* Sidebar */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child {
    background: var(--sidebar) !important;
}

[data-testid="stSidebar"] {
    width: 300px !important;
    min-width: 300px !important;
    max-width: 300px !important;
    border-right: 2px solid #d7dce5 !important;
    box-shadow: 6px 0 18px rgba(15, 23, 42, 0.05) !important;
    z-index: 20 !important;
}

[data-testid="stSidebar"] > div:first-child {
    width: 300px !important;
    min-width: 300px !important;
    max-width: 300px !important;
}

[data-testid="stSidebar"] * {
    color: #111827 !important;
}

.sidebar-title {
    padding: 14px 4px 18px;
    color: #111827 !important;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 0.01em;
}

.history-title {
    margin: 14px 4px 12px;
    padding-bottom: 10px;
    border-bottom: 2px solid var(--accent);
    color: var(--accent) !important;
    font-size: 14px;
    font-weight: 700;
}

.sidebar-caption {
    color: #a1a1aa !important;
    font-size: 12px;
    padding: 0 4px 8px;
}

[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    min-height: 44px !important;
    justify-content: flex-start !important;
    text-align: left !important;
    background: #ffffff !important;
    border: 1px solid #edf0f5 !important;
    border-radius: 10px !important;
    color: #111827 !important;
    padding: 10px 12px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03) !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease, background 0.15s ease !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #ffffff !important;
    border-color: #93c5fd !important;
    box-shadow: 0 0 0 1px #93c5fd !important;
}

[data-testid="stSidebar"] .stButton > button:disabled {
    background: #ffffff !important;
    border-color: var(--accent) !important;
    color: #111827 !important;
    opacity: 1 !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}

[data-testid="stSidebar"] hr {
    border-color: var(--sidebar-border) !important;
    margin: 12px 0 !important;
}

[data-testid="stSidebar"] [data-testid="stExpander"] {
    border: 1px solid var(--sidebar-border) !important;
    border-radius: 10px !important;
    background: #ffffff !important;
}

[data-testid="stSidebar"] .stAlert {
    background: #ffffff !important;
    border: 1px solid var(--sidebar-border) !important;
    border-radius: 8px !important;
}

/* Main chat layout */
.chat-shell {
    min-height: calc(100vh - 126px);
    background: #ffffff;
    padding: 0;
}

.chat-topbar {
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 20px;
    background: #ffffff;
}

.chat-title {
    width: min(100%, 760px);
    color: var(--text);
    font-size: 16px;
    font-weight: 650;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.chat-content {
    width: min(100%, 760px);
    margin: 0 auto;
    padding: 0 20px 100px;
}

.empty-state {
    padding: 0 0 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.chat-shell [data-testid="stMarkdownContainer"] {
    margin: 0 !important;
}

.chat-shell [data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

.empty-title {
    font-size: 24px;
    line-height: 1.25;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 8px;
}

.empty-subtitle {
    color: var(--muted);
    font-size: 14px;
    margin-bottom: 16px;
}

.prompt-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
    width: min(100%, 620px);
}

.prompt-card {
    border: 1px solid #eeeeee;
    border-radius: 10px;
    padding: 10px 12px;
    background: #fbfbfb;
    color: #6b7280;
    text-align: left;
    font-size: 13px;
}

/* Plain text messages */
.plain-message {
    padding: 18px 0;
    border-bottom: 1px solid #f0f0f0;
}

.plain-message:last-child {
    border-bottom: none;
}

.message-label {
    margin-bottom: 8px;
    color: var(--muted);
    font-size: 13px;
    font-weight: 600;
}

.message-content {
    color: var(--text);
    font-size: 15px;
    line-height: 1.75;
    word-break: break-word;
}

.user-message .message-content {
    background: #f7f7f8;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 12px 14px;
}

.assistant-message .message-content {
    padding: 2px 0;
}

/* Chat input */
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"],
[data-testid="stChatInput"] {
    background: #ffffff !important;
}

[data-testid="stBottomBlockContainer"] {
    padding: 0 !important;
}

[data-testid="stChatInput"] {
    padding: 14px 20px 18px !important;
    border-top: none !important;
}

[data-testid="stChatInput"] > div {
    background-color: #ffffff !important;
}

[data-testid="stChatInput"] > div {
    width: min(100%, 760px) !important;
    min-height: 74px !important;
    margin: 0 auto !important;
    background: #ffffff !important;
    border: 1px solid #dfe3ea !important;
    border-radius: 18px !important;
    box-shadow: 0 4px 18px rgba(15, 23, 42, 0.12) !important;
    padding: 14px 16px !important;
}

[data-testid="stChatInput"] textarea {
    color: var(--text) !important;
    background: transparent !important;
    border: none !important;
    font-size: 15px !important;
    line-height: 1.5 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #8e8ea0 !important;
}

[data-testid="stChatInput"] button {
    background-color: #111111 !important;
    color: #ffffff !important;
    border-radius: 10px !important;
}

[data-testid="stChatInput"] button:hover {
    background: #000000 !important;
}

.stSpinner {
    width: min(100%, 760px) !important;
    margin: 0 auto !important;
    padding: 0 20px !important;
}

@media (max-width: 760px) {
    .chat-content {
        padding-left: 14px;
        padding-right: 14px;
    }

    .prompt-grid {
        grid-template-columns: 1fr;
    }
}
</style>
"""
