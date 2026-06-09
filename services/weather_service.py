import requests
from config.settings import AMAP_API_KEY


def city_to_adcode(city: str) -> str:
    """将城市中文名转换为高德 adcode。

    Args:
        city: 城市中文名称，如"北京"

    Returns:
        adcode 字符串，如 "110000"

    Raises:
        ValueError: 城市名无法识别时抛出
    """
    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        "key": AMAP_API_KEY,
        "address": city,
        "city": city,
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()

        if data.get("status") == "1" and data.get("geocodes"):
            return data["geocodes"][0]["adcode"]

        raise ValueError(f"无法识别城市: {city}，请输入准确的城市名称")
    except requests.Timeout:
        raise Exception("查询超时，请稍后重试")
    except requests.RequestException as e:
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
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()

        if data.get("status") == "1" and data.get("lives"):
            return data["lives"][0]

        raise Exception(f"获取天气失败: {data.get('info', '未知错误')}")
    except requests.Timeout:
        raise Exception("查询超时，请稍后重试")
    except requests.RequestException as e:
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
