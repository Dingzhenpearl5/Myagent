import logging
import time

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage

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

logger = logging.getLogger(__name__)

# 系统提示词
SYSTEM_PROMPT = """你是一个企业综合信息查询助手。你可以帮助用户查询以下信息：

1. **天气查询**：使用 get_weather 工具查询指定城市的实时天气
2. **股票查询**：使用 get_stock 工具查询 A 股股票的实时行情
3. **内部资料查询**：使用 query_internal_docs 工具查询公司内部文档

重要规则：
- 如果用户只是打招呼或闲聊，直接友好回复，不要调用任何工具。
- 如果用户询问公司制度、员工手册、报销、请假、考勤、居家办公、信息安全、绩效晋升、培训学习、离职交接等内部资料，必须调用 query_internal_docs 工具，并在回答中提示「已查阅内部资料」。
- 如果用户的问题超出你的能力范围（如要求写论文、写代码等），礼貌说明你只能进行信息查询。
- 股票相关回答必须提醒「以上信息仅供参考，不构成投资建议」。
- 用户信息不足时（如只说"股价多少"而不指定股票），请向用户追问并确认。
- 回答要简洁、准确，基于工具返回的真实数据，不要编造信息。"""


def create_agent():
    """创建并返回 LangGraph ReAct Agent。

    初始化 LLM（DeepSeek）、注册所有工具、组装 Agent。
    对话历史以 messages 列表形式从外部传入。

    Returns:
        一个可被 invoke({"messages": [...]}) 调用的 agent 对象
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

    # 创建 LangGraph ReAct Agent
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT,
    )

    return agent


def invoke_agent(agent, user_input: str, history: list[dict]) -> str:
    """调用 Agent 处理用户输入。

    Args:
        agent: create_agent() 创建的 agent 实例
        user_input: 用户的当前输入
        history: 对话历史，格式 [{"role": "user"/"assistant", "content": "..."}]

    Returns:
        Agent 的最终文本回答
    """
    # 把对话历史转换为 LangChain 的消息对象列表
    messages = []
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))

    # 追加当前用户输入
    messages.append(HumanMessage(content=user_input))

    # 调用 Agent
    started_at = time.perf_counter()
    try:
        result = agent.invoke({"messages": messages})
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.info("agent.invoke success messages=%s elapsed_ms=%.0f", len(messages), elapsed_ms)
    except Exception:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.exception("agent.invoke failed messages=%s elapsed_ms=%.0f", len(messages), elapsed_ms)
        raise

    # 提取最后一条 AI 消息内容
    if "messages" in result and result["messages"]:
        last_msg = result["messages"][-1]
        return last_msg.content if hasattr(last_msg, "content") else str(last_msg)

    return ""
