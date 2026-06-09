from services.stock_service import search_stock, query_stock


def test_search_stock_by_code():
    """测试按代码搜索"""
    result = search_stock("000001")
    assert result is not None
    assert result["名称"] == "平安银行"
    print("✅ 按代码搜索测试通过")


def test_search_stock_by_name():
    """测试按名称搜索"""
    result = search_stock("平安银行")
    assert result is not None
    assert result["代码"] == "000001"
    print("✅ 按名称搜索测试通过")


def test_search_stock_fuzzy():
    """测试模糊搜索"""
    result = search_stock("茅台")
    assert result is not None
    assert "茅台" in result["名称"]
    print("✅ 模糊搜索测试通过")


def test_query_stock():
    """测试股票查询含风险提示"""
    result = query_stock("000001")
    assert "平安银行" in result
    assert "仅供参考，不构成投资建议" in result
    print("✅ 风险提示测试通过")


def test_query_stock_not_found():
    """测试未找到股票"""
    result = query_stock("000000")
    assert "未找到" in result
    print("✅ 未找到股票处理测试通过")


if __name__ == "__main__":
    test_search_stock_by_code()
    test_search_stock_by_name()
    test_search_stock_fuzzy()
    test_query_stock()
    test_query_stock_not_found()
