import logging

from langchain.tools import tool
from services.rag_service import search_internal_docs

logger = logging.getLogger(__name__)


@tool
def query_internal_docs(query: str) -> str:
    """搜索公司内部文档知识库。

    当用户询问公司制度、员工手册、报销、请假、考勤、居家办公、
    信息安全、绩效晋升、培训学习、离职交接等内部资料时，必须使用此工具。

    Args:
        query: 用户的具体问题或关键词

    Returns:
        基于内部资料命中的相关片段和来源文件名
    """
    normalized_query = (query or "").strip()
    if not normalized_query:
        return "请说明要查阅的内部资料问题，例如：报销标准、请假流程、信息安全要求。"

    try:
        return search_internal_docs(normalized_query)
    except Exception:
        logger.exception("internal docs tool failed query_len=%s", len(normalized_query))
        return "内部资料查询暂时不可用，请稍后重试。"
