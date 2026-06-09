from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from config.settings import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    MODEL_NAME,
    TEMPERATURE,
    MAX_TOKENS,
)
from tools.weather_tool import get_weather
from tools.stock_tool import get_stock
from tools.rag_tool import query_internal_docs

# 系统提示词
SYSTEM_PROMPT = """你是一个企业综合信息查询助手。你可以帮助用户查询以下信息：

1. **天气查询**：使用 get_weather 工具查询指定城市的实时天气
2. **股票查询**：使用 get_stock 工具查询 A 股股票的实时行情
3. **内部资料查询**：使用 query_internal_docs 工具查询公司内部文档

重要规则：
- 如果用户只是打招呼或闲聊，直接友好回复，不要调用任何工具。
- 如果用户的问题超出你的能力范围（如要求写论文、写代码等），礼貌说明你只能进行信息查询。
- 股票相关回答必须提醒「以上信息仅供参考，不构成投资建议」。
- 用户信息不足时（如只说"股价多少"而不指定股票），请向用户追问并确认。
- 回答要简洁、准确，基于工具返回的真实数据，不要编造信息。"""


def create_agent() -> AgentExecutor:
    """创建并返回配置好的 Agent Executor。

    初始化 LLM（DeepSeek）、注册所有工具、组装 Agent。

    Returns:
        AgentExecutor 实例，对话历史由外部 session_state 管理
    """
    # 初始化 LLM
    llm = ChatOpenAI(
        model=MODEL_NAME,
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    # 注册全部工具
    tools = [
        get_weather,
        get_stock,
        query_internal_docs,
    ]

    # 构建 Prompt（chat_history 由外部传入）
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # 创建 Tool Calling Agent
    agent = create_tool_calling_agent(llm, tools, prompt)

    # 包装为 AgentExecutor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        handle_parsing_errors=True,
    )

    return agent_executor
