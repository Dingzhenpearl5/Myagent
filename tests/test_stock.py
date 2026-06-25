from unittest.mock import patch

import pandas as pd

from services import stock_service
from services.stock_service import query_stock, search_stock


def _stock_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "代码": "000001",
                "名称": "平安银行",
                "最新价": 10.5,
                "涨跌幅": 1.2,
                "涨跌额": 0.12,
                "成交量": 10000,
                "今开": 10.2,
                "昨收": 10.38,
                "最高": 10.8,
                "最低": 10.1,
            },
            {
                "代码": "600519",
                "名称": "贵州茅台",
                "最新价": 1500,
                "涨跌幅": -0.5,
                "涨跌额": -7.5,
                "成交量": 2000,
                "今开": 1510,
                "昨收": 1507.5,
                "最高": 1520,
                "最低": 1495,
            },
        ]
    )


def setup_function():
    stock_service._STOCK_CACHE.update({"df": None, "timestamp": 0, "expires": 60})


def test_search_stock_by_code():
    """测试按代码搜索"""
    with patch("services.stock_service.ak.stock_zh_a_spot_em", return_value=_stock_df()):
        result = search_stock("000001")

    assert result is not None
    assert result["名称"] == "平安银行"
    print("✅ 按代码搜索测试通过")


def test_search_stock_by_name():
    """测试按名称搜索"""
    with patch("services.stock_service.ak.stock_zh_a_spot_em", return_value=_stock_df()):
        result = search_stock("平安银行")

    assert result is not None
    assert result["代码"] == "000001"
    print("✅ 按名称搜索测试通过")


def test_search_stock_fuzzy():
    """测试模糊搜索"""
    with patch("services.stock_service.ak.stock_zh_a_spot_em", return_value=_stock_df()):
        result = search_stock("茅台")

    assert result is not None
    assert "茅台" in result["名称"]
    print("✅ 模糊搜索测试通过")


def test_query_stock():
    """测试股票查询含风险提示"""
    with patch("services.stock_service.ak.stock_zh_a_spot_em", return_value=_stock_df()):
        result = query_stock("000001")

    assert "平安银行" in result
    assert "仅供参考，不构成投资建议" in result
    print("✅ 风险提示测试通过")


def test_query_stock_not_found():
    """测试未找到股票"""
    with patch("services.stock_service.ak.stock_zh_a_spot_em", return_value=_stock_df()):
        result = query_stock("000000")

    assert "未找到" in result
    print("✅ 未找到股票处理测试通过")


def test_query_stock_fallback_source():
    """测试主行情接口失败后降级到备用接口"""
    with patch("services.stock_service.ak.stock_zh_a_spot_em", side_effect=Exception("primary failed")), patch(
        "services.stock_service.ak.stock_zh_a_spot", return_value=_stock_df()
    ):
        result = query_stock("000001")

    assert "平安银行" in result


if __name__ == "__main__":
    test_search_stock_by_code()
    test_search_stock_by_name()
    test_search_stock_fuzzy()
    test_query_stock()
    test_query_stock_not_found()
    test_query_stock_fallback_source()
