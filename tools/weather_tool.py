import logging

from langchain.tools import tool
from services.weather_service import query_weather

logger = logging.getLogger(__name__)


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
    normalized_city = (city or "").strip()
    if not normalized_city:
        return "请提供要查询天气的城市名称，例如：北京、上海、深圳。"

    try:
        return query_weather(normalized_city)
    except Exception:
        logger.exception("weather tool failed city_len=%s", len(normalized_city))
        return "天气查询工具暂时不可用，请稍后重试或检查城市名称是否正确。"
