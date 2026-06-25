import logging
import time

import akshare as ak
import pandas as pd

logger = logging.getLogger(__name__)

# 内存缓存，60 秒内重复查询不重新拉取全市场数据
_STOCK_CACHE = {"df": None, "timestamp": 0, "expires": 60}


def _normalize_code(raw_code: str) -> str:
    """去掉股票代码中的交易所前缀（sh/sz/bj），保留 6 位数字。"""
    if isinstance(raw_code, str):
        return raw_code.strip().lower().replace("sh", "").replace("sz", "").replace("bj", "")
    return str(raw_code)


def _get_all_stocks() -> pd.DataFrame:
    """获取全市场 A 股数据，带 60 秒缓存。

    优先使用 stock_zh_a_spot_em，失败时降级到 stock_zh_a_spot。
    """
    now = time.time()
    if _STOCK_CACHE["df"] is not None and now - _STOCK_CACHE["timestamp"] < _STOCK_CACHE["expires"]:
        logger.info("stock.cache hit")
        return _STOCK_CACHE["df"]

    try:
        started_at = time.perf_counter()
        df = ak.stock_zh_a_spot_em()
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        _STOCK_CACHE["df"] = df
        _STOCK_CACHE["timestamp"] = now
        logger.info("stock.fetch primary success rows=%s elapsed_ms=%.0f", len(df), elapsed_ms)
        return df
    except Exception as e:
        logger.warning("stock.fetch primary failed error=%s", type(e).__name__)

    try:
        started_at = time.perf_counter()
        df = ak.stock_zh_a_spot()
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        _STOCK_CACHE["df"] = df
        _STOCK_CACHE["timestamp"] = now
        logger.info("stock.fetch fallback success rows=%s elapsed_ms=%.0f", len(df), elapsed_ms)
        return df
    except Exception as e:
        logger.exception("stock.fetch fallback failed")
        raise Exception(f"无法获取股票数据: {str(e)}")


def _search_in_dataframe(df: pd.DataFrame, keyword: str) -> dict | None:
    """在 DataFrame 中按代码或名称搜索股票。"""
    if df is None or df.empty:
        return None

    df = df.copy()
    df["代码_标准"] = df["代码"].apply(_normalize_code)
    keyword_norm = _normalize_code(keyword)

    # 1. 精确匹配代码（兼容 sh/sz/bj 前缀）
    match = df[df["代码_标准"] == keyword_norm]
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


def search_stock(keyword: str) -> dict | None:
    """在 A 股市场中搜索股票。

    Args:
        keyword: 股票名称或6位代码，如"平安银行"、"000001"、"茅台"

    Returns:
        匹配到的股票信息字典，未找到则返回 None
    """
    df = _get_all_stocks()
    return _search_in_dataframe(df, keyword)


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
        f"\n风险提示：以上信息仅供参考，不构成投资建议。"
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
