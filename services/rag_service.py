# 内部资料 RAG 服务 — 扩展阶段填充实现
# 当前为空实现，供后续 RAG 知识库扩展使用

"""
扩展阶段实现内容：

1. 文档加载：PyMuPDF (PDF) + python-docx (Word)
2. 文本分块：RecursiveCharacterTextSplitter
3. Embedding：BGE 中文向量模型 / 通义千问 Embedding / 智谱 Embedding
4. 向量存储：Chroma（推荐）或 FAISS
5. 检索召回：similarity_search(k=3)
"""


def search_internal_docs(query: str) -> str:
    """搜索内部文档知识库（当前为空实现）。"""
    return "当前版本暂未接入内部资料查询功能，后续可通过 RAG 知识库实现。"
