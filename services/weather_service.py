import logging
import time

import requests
from config.settings import AMAP_API_KEY

logger = logging.getLogger(__name__)

# 常见城市 adcode 本地兜底映射（高德 Web 服务 Key 受限时可用）
CITY_ADCODE_MAP = {
    "北京": "110000", "北京市": "110000",
    "上海": "310000", "上海市": "310000",
    "广州": "440100", "广州市": "440100",
    "深圳": "440300", "深圳市": "440300",
    "杭州": "330100", "杭州市": "330100",
    "南京": "320100", "南京市": "320100",
    "成都": "510100", "成都市": "510100",
    "武汉": "420100", "武汉市": "420100",
    "西安": "610100", "西安市": "610100",
    "重庆": "500000", "重庆市": "500000",
    "天津": "120000", "天津市": "120000",
    "苏州": "320500", "苏州市": "320500",
    "郑州": "410100", "郑州市": "410100",
    "长沙": "430100", "长沙市": "430100",
    "青岛": "370200", "青岛市": "370200",
    "宁波": "330200", "宁波市": "330200",
    "厦门": "350200", "厦门市": "350200",
}


def city_to_adcode(city: str) -> str:
    """将城市中文名转换为高德 adcode。"""
    # 优先本地兜底，避免高德地理编码 API Key 权限问题
    if city in CITY_ADCODE_MAP:
        return CITY_ADCODE_MAP[city]

    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        "key": AMAP_API_KEY,
        "address": city,
        "city": city,
    }

    try:
        started_at = time.perf_counter()
        resp = requests.get(url, params=params, timeout=10)
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        data = resp.json()

        if data.get("status") == "1" and data.get("geocodes"):
            logger.info("amap.geocode success elapsed_ms=%.0f", elapsed_ms)
            return data["geocodes"][0]["adcode"]

        # 返回高德真实错误信息，便于排查
        error_info = data.get("info", "未知错误")
        infocode = data.get("infocode", "")
        logger.warning("amap.geocode failed infocode=%s info=%s elapsed_ms=%.0f", infocode, error_info, elapsed_ms)
        if infocode == "10009":
            raise ValueError(
                "高德 API Key 平台不匹配（USERKEY_PLAT_NOMATCH）。"
                "请前往 https://console.amap.com 为该 Key 添加「Web服务API」权限。"
            )
        raise ValueError(f"无法识别城市: {city}（高德返回：{error_info}）")
    except requests.Timeout:
        logger.warning("amap.geocode timeout")
        raise Exception("查询超时，请稍后重试")
    except requests.RequestException as e:
        logger.warning("amap.geocode request failed error=%s", type(e).__name__)
        raise Exception(f"网络请求失败: {str(e)}")


def get_realtime_weather(adcode: str) -> dict:
    """根据 adcode 获取实时天气信息。

    Args:
        adcode: 城市编码，如 "110000"

    Returns:
        实时天气数据字典

    Raises:
        Exception: API 调用失败时抛出
    """
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    params = {
        "key": AMAP_API_KEY,
        "city": adcode,
        "extensions": "base",  # base=实时天气, all=预报天气
    }

    try:
        started_at = time.perf_counter()
        resp = requests.get(url, params=params, timeout=10)
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        data = resp.json()

        if data.get("status") == "1" and data.get("lives"):
            logger.info("amap.weather success elapsed_ms=%.0f", elapsed_ms)
            return data["lives"][0]

        error_info = data.get("info", "未知错误")
        infocode = data.get("infocode", "")
        logger.warning("amap.weather failed infocode=%s info=%s elapsed_ms=%.0f", infocode, error_info, elapsed_ms)
        if infocode == "10009":
            raise Exception(
                "高德 API Key 平台不匹配（USERKEY_PLAT_NOMATCH）。"
                "请前往 https://console.amap.com 为该 Key 添加「Web服务API」权限。"
            )
        raise Exception(f"获取天气失败: {error_info}")
    except requests.Timeout:
        logger.warning("amap.weather timeout")
        raise Exception("查询超时，请稍后重试")
    except requests.RequestException as e:
        logger.warning("amap.weather request failed error=%s", type(e).__name__)
        raise Exception(f"网络请求失败: {str(e)}")


def format_weather(raw: dict) -> str:
    """将原始天气 JSON 格式化为可读字符串。

    Args:
        raw: get_realtime_weather 返回的原始字典

    Returns:
        格式化的天气信息字符串
    """
    return (
        f"城市: {raw.get('province', '')}{raw.get('city', '')}\n"
        f"天气: {raw.get('weather', '未知')}\n"
        f"温度: {raw.get('temperature', '未知')}℃\n"
        f"湿度: {raw.get('humidity', '未知')}%\n"
        f"风向: {raw.get('winddirection', '未知')}\n"
        f"风力: {raw.get('windpower', '未知')}级\n"
        f"数据发布时间: {raw.get('reporttime', '未知')}"
    )


def query_weather(city: str) -> str:
    """完整的天气查询流程：城市名 → adcode → 天气数据 → 格式化。

    Args:
        city: 城市中文名称

    Returns:
        格式化的天气信息字符串或错误信息
    """
    if not AMAP_API_KEY:
        return "高德 API Key 未配置，请在 .env 文件中设置 AMAP_API_KEY。"

    try:
        adcode = city_to_adcode(city)
        raw = get_realtime_weather(adcode)
        return format_weather(raw)
    except Exception as e:
        return f"天气查询失败: {str(e)}"
