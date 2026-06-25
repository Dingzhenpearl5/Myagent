import logging

from langchain.tools import tool
from services.stock_service import query_stock

logger = logging.getLogger(__name__)


@tool
def get_stock(stock_query: str) -> str:
    """查询 A 股股票的实时行情。

    当用户询问股价、涨跌、股票行情、或提到6位数字的股票代码时，
    使用此工具通过 AkShare 获取 A 股实时行情数据。

    Args:
        stock_query: 股票名称或6位数字代码，例如"平安银行"、"000001"、"茅台"

    Returns:
        格式化的股票行情信息字符串，包含最新价、涨跌幅、成交量等，
        末尾自动附带风险提示。
    """
    normalized_query = (stock_query or "").strip()
    if not normalized_query:
        return "请提供要查询的 A 股股票名称或 6 位代码，例如：平安银行、000001。"

    try:
        return query_stock(normalized_query)
    except Exception:
        logger.exception("stock tool failed query_len=%s", len(normalized_query))
        return "股票查询工具暂时不可用，请稍后重试或检查股票名称/代码是否正确。"
