from langchain.tools import tool
from services.stock_service import query_stock


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
    return query_stock(stock_query)
