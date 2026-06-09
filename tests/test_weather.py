from services.weather_service import city_to_adcode, query_weather


def test_city_to_adcode():
    """测试城市名转 adcode"""
    assert city_to_adcode("北京") == "110000"
    assert city_to_adcode("上海") == "310000"
    print("✅ city_to_adcode 测试通过")


def test_query_weather():
    """测试天气查询"""
    result = query_weather("北京")
    assert "城市" in result
    assert "温度" in result
    assert "天气" in result
    print("✅ query_weather 测试通过")


def test_query_weather_invalid_city():
    """测试无效城市名的错误处理"""
    result = query_weather("不存在的城市名称123456")
    assert "失败" in result or "无法" in result
    print("✅ 无效城市名处理测试通过")


if __name__ == "__main__":
    test_city_to_adcode()
    test_query_weather()
    test_query_weather_invalid_city()
