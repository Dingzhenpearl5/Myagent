"""测试 Agent 行为。

注意：这些测试需要 DEEPSEEK_API_KEY 真实可用才会通过。
可使用 mock 工具来避免实际 API 调用。
"""
import os
from unittest.mock import Mock

from langchain_core.messages import HumanMessage, AIMessage

from agent.agent_factory import create_agent, invoke_agent


def _has_api_key() -> bool:
    return bool(os.getenv("DEEPSEEK_API_KEY"))


def test_agent_creation():
    """测试 Agent 能否正常创建"""
    agent = create_agent()
    assert agent is not None
    print("✅ Agent 创建测试通过")


def test_invoke_agent_converts_history_messages():
    """测试 invoke_agent 将历史和当前输入转换为 LangChain 消息。"""
    agent = Mock()
    agent.invoke.return_value = {"messages": [AIMessage(content="收到")]}
    history = [
        {"role": "user", "content": "北京天气怎么样？"},
        {"role": "assistant", "content": "北京今天晴。"},
    ]

    answer = invoke_agent(agent=agent, user_input="那上海呢？", history=history)

    assert answer == "收到"
    payload = agent.invoke.call_args.args[0]
    messages = payload["messages"]
    assert len(messages) == 3
    assert isinstance(messages[0], HumanMessage)
    assert isinstance(messages[1], AIMessage)
    assert isinstance(messages[2], HumanMessage)
    assert messages[2].content == "那上海呢？"


def test_agent_weather_intent():
    """测试 Agent 天气意图识别。

    如需验证 Agent 是否正确调用工具，可在测试模式下使用
    return_intermediate_steps=True，或使用 mock 工具记录调用参数。
    """
    if not _has_api_key():
        print("⏭️ 跳过 weather 意图测试（未配置 DEEPSEEK_API_KEY）")
        return

    agent = create_agent()
    answer = invoke_agent(
        agent=agent,
        user_input="北京天气怎么样？",
        history=[],
    )
    # 验证回答非空
    assert answer and len(answer) > 0
    print(f"✅ 天气意图回答：{answer[:50]}...")


def test_agent_stock_intent():
    """测试 Agent 股票意图识别。"""
    if not _has_api_key():
        print("⏭️ 跳过 stock 意图测试（未配置 DEEPSEEK_API_KEY）")
        return

    agent = create_agent()
    answer = invoke_agent(
        agent=agent,
        user_input="000001 最新股价？",
        history=[],
    )
    assert answer and len(answer) > 0
    print(f"✅ 股票意图回答：{answer[:50]}...")


def test_agent_chitchat():
    """测试闲聊场景。"""
    if not _has_api_key():
        print("⏭️ 跳过闲聊测试（未配置 DEEPSEEK_API_KEY）")
        return

    agent = create_agent()
    answer = invoke_agent(
        agent=agent,
        user_input="你好！",
        history=[],
    )
    assert answer and len(answer) > 0
    print(f"✅ 闲聊回答：{answer[:50]}...")


def test_agent_history():
    """测试多轮对话上下文保持。"""
    if not _has_api_key():
        print("⏭️ 跳过多轮对话测试（未配置 DEEPSEEK_API_KEY）")
        return

    agent = create_agent()
    history = [
        {"role": "user", "content": "北京今天天气怎么样？"},
        {"role": "assistant", "content": "北京今天晴，温度 25℃。"},
    ]
    answer = invoke_agent(
        agent=agent,
        user_input="那明天呢？",
        history=history,
    )
    assert answer and len(answer) > 0
    print(f"✅ 多轮对话回答：{answer[:50]}...")


if __name__ == "__main__":
    test_agent_creation()
    test_agent_weather_intent()
    test_agent_stock_intent()
    test_agent_chitchat()
    test_agent_history()
