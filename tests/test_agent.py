from agent.agent_factory import create_agent


def test_agent_creation():
    """测试 Agent 能否正常创建"""
    agent = create_agent()
    assert agent is not None
    print("✅ Agent 创建测试通过")


def test_agent_weather_intent():
    """测试 Agent 天气意图识别（通过 intermediate_steps 验证工具调用）

    在测试模式下验证 Agent 是否正确识别天气问题并调用对应工具。
    """
    agent = create_agent()
    result = agent.invoke(
        {
            "input": "北京天气怎么样？",
            "chat_history": [],
        },
        return_intermediate_steps=True,  # 返回中间步骤用于验证
    )

    # 验证有工具被调用
    assert len(result["intermediate_steps"]) > 0
    # 验证第一个工具调用是 get_weather
    tool_name = result["intermediate_steps"][0][0].tool
    assert tool_name == "get_weather"
    print(f"✅ 天气意图识别测试通过，调用了工具: {tool_name}")


def test_agent_stock_intent():
    """测试 Agent 股票意图识别"""
    agent = create_agent()
    result = agent.invoke(
        {
            "input": "000001 最新股价？",
            "chat_history": [],
        },
        return_intermediate_steps=True,
    )

    assert len(result["intermediate_steps"]) > 0
    tool_name = result["intermediate_steps"][0][0].tool
    assert tool_name == "get_stock"
    print(f"✅ 股票意图识别测试通过，调用了工具: {tool_name}")


def test_agent_chitchat():
    """测试闲聊场景不调工具"""
    agent = create_agent()
    result = agent.invoke(
        {
            "input": "你好！",
            "chat_history": [],
        },
        return_intermediate_steps=True,
    )

    # 闲聊不应调用任何工具
    assert len(result["intermediate_steps"]) == 0
    assert len(result["output"]) > 0
    print("✅ 闲聊无工具调用测试通过")


if __name__ == "__main__":
    test_agent_creation()
    test_agent_weather_intent()
    test_agent_stock_intent()
    test_agent_chitchat()
