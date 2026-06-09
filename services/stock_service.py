import akshare as ak


def search_stock(keyword: str) -> dict | None:
    """在 A 股市场中搜索股票。

    匹配优先级：代码精确匹配 > 名称精确匹配 > 名称模糊匹配。

    Args:
        keyword: 股票名称或6位代码，如"平安银行"、"000001"、"茅台"

    Returns:
        匹配到的股票信息字典，未找到则返回 None
    """
    try:
        df = ak.stock_zh_a_spot_em()

        # 1. 精确匹配代码
        match = df[df["代码"] == keyword]
        if not match.empty:
            return match.iloc[0].to_dict()

        # 2. 精确匹配名称
        match = df[df["名称"] == keyword]
        if not match.empty:
            return match.iloc[0].to_dict()

        # 3. 模糊匹配名称
        match = df[df["名称"].str.contains(keyword, na=False)]
        if not match.empty:
            return match.iloc[0].to_dict()

        return None
    except Exception:
        return None


def format_stock(info: dict) -> str:
    """将股票数据字典格式化为可读字符串，末尾自动附加风险提示。

    Args:
        info: search_stock 返回的股票信息字典

    Returns:
        格式化的股票行情字符串
    """
    result = (
        f"股票名称: {info.get('名称', '未知')}\n"
        f"股票代码: {info.get('代码', '未知')}\n"
        f"最新价: {info.get('最新价', '未知')} 元\n"
        f"涨跌幅: {info.get('涨跌幅', '未知')}%\n"
        f"涨跌额: {info.get('涨跌额', '未知')} 元\n"
        f"成交量: {info.get('成交量', '未知')} 手\n"
        f"今开价: {info.get('今开', '未知')} 元\n"
        f"昨收价: {info.get('昨收', '未知')} 元\n"
        f"最高价: {info.get('最高', '未知')} 元\n"
        f"最低价: {info.get('最低', '未知')} 元\n"
        f"\n⚠️ 以上信息仅供参考，不构成投资建议。"
    )
    return result


def query_stock(keyword: str) -> str:
    """完整的股票查询流程：搜索 → 格式化。

    Args:
        keyword: 股票名称或代码

    Returns:
        格式化的股票行情字符串或错误信息
    """
    try:
        info = search_stock(keyword)
        if info is None:
            return (
                f"未找到与「{keyword}」相关的 A 股股票。\n"
                f"请检查股票名称或 6 位代码是否正确。"
            )
        return format_stock(info)
    except Exception as e:
        return f"股票查询失败: {str(e)}"
