from langchain.tools import tool


@tool
def query_internal_docs(query: str) -> str:
    """搜索公司内部文档知识库。

    当用户询问公司内部制度、流程、文档、员工手册、报销、请假、
    产品资料等内容时触发。MVP 阶段暂不支持，后续通过 RAG 实现。

    Args:
        query: 用户的具体问题或关键词

    Returns:
        固定提示文案，告知用户该功能尚未接入
    """
    return "当前版本暂未接入内部资料查询功能，后续可通过 RAG 知识库实现。"
