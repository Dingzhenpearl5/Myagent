from langchain.tools import tool
from services.weather_service import query_weather


@tool
def get_weather(city: str) -> str:
    """查询指定城市的实时天气。

    当用户询问某个城市的天气、温度、冷热、是否下雨等问题时，
    使用此工具查询高德天气 API 获取实时天气数据。

    Args:
        city: 城市中文名称，例如"北京"、"上海"、"深圳"

    Returns:
        格式化的天气信息字符串，包含温度、天气状况、湿度、风力等
    """
    return query_weather(city)
