from unittest.mock import Mock, patch

import requests

from services.weather_service import city_to_adcode, query_weather


def test_city_to_adcode():
    """测试城市名转 adcode"""
    assert city_to_adcode("北京") == "110000"
    assert city_to_adcode("上海") == "310000"
    print("✅ city_to_adcode 测试通过")


def test_query_weather():
    """测试天气查询"""
    mock_response = Mock()
    mock_response.json.return_value = {
        "status": "1",
        "lives": [
            {
                "province": "北京",
                "city": "北京市",
                "weather": "晴",
                "temperature": "25",
                "humidity": "40",
                "winddirection": "北",
                "windpower": "3",
                "reporttime": "2026-06-25 10:00:00",
            }
        ],
    }

    with patch("services.weather_service.AMAP_API_KEY", "test-key"), patch(
        "services.weather_service.requests.get", return_value=mock_response
    ) as mock_get:
        result = query_weather("北京")

    assert mock_get.call_count == 1
    assert "城市" in result
    assert "温度" in result
    assert "天气" in result
    print("✅ query_weather 测试通过")


def test_query_weather_invalid_city():
    """测试无效城市名的错误处理"""
    mock_response = Mock()
    mock_response.json.return_value = {
        "status": "0",
        "info": "INVALID_USER_KEY",
        "infocode": "10001",
    }

    with patch("services.weather_service.AMAP_API_KEY", "test-key"), patch(
        "services.weather_service.requests.get", return_value=mock_response
    ):
        result = query_weather("不存在的城市名称123456")

    assert "失败" in result or "无法" in result
    print("✅ 无效城市名处理测试通过")


def test_query_weather_timeout():
    """测试天气接口超时错误映射"""
    with patch("services.weather_service.AMAP_API_KEY", "test-key"), patch(
        "services.weather_service.requests.get", side_effect=requests.Timeout
    ):
        result = query_weather("北京")

    assert "查询超时" in result


if __name__ == "__main__":
    test_city_to_adcode()
    test_query_weather()
    test_query_weather_invalid_city()
    test_query_weather_timeout()
