"""TCL 知识库 API 查询服务。"""

import json
import logging
import os
import urllib.error
import urllib.request
from typing import Any

logger = logging.getLogger(__name__)

BASE_URL = "https://aigc-gateway.tcl.com/knowledge/v1/0/api"
OCTOPUS_BASE_URL = "https://aigc-gateway.tcl.com/knowledge/v1/0/octopus/api"
DEFAULT_TOP_K = 5
DEFAULT_TIMEOUT = 30


def _get_token() -> str:
    """从环境变量读取 TCL 知识库访问 Token。"""
    token = os.environ.get("TCL_TOKEN", "").strip()
    if not token:
        return ""
    return token if token.lower().startswith("bearer ") else f"bearer {token}"


def is_tcl_kb_configured() -> bool:
    """判断是否已配置 TCL 知识库访问 Token。"""
    return bool(_get_token())


def _request_json(
    method: str,
    url: str,
    body: dict[str, Any] | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """发送 JSON API 请求。"""
    token = _get_token()
    if not token:
        raise RuntimeError("未配置 TCL_TOKEN")

    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method=method,
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"TCL 知识库 HTTP {exc.code}: {error_body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"TCL 知识库网络请求失败: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("TCL 知识库返回了非 JSON 响应") from exc

    if isinstance(result, dict) and result.get("code") in (200, 1000):
        data = result.get("data", result)
        return data if isinstance(data, dict) else {"data": data}
    return result if isinstance(result, dict) else {"data": result}


def list_knowledge_bases() -> list[dict[str, Any]]:
    """列出当前 Token 有权限访问的知识库。"""
    result = _request_json("POST", f"{BASE_URL}/base/query", {})
    records = result.get("records", [])
    return records if isinstance(records, list) else []


def _get_knowledge_base_detail(knowledge_id: int) -> dict[str, Any]:
    """获取知识库详情。"""
    return _request_json("GET", f"{BASE_URL}/base/{knowledge_id}")


def _search_vector_results(
    knowledge_id: int,
    query: str,
    top_k: int,
    detail: dict[str, Any],
) -> list[dict[str, Any]]:
    """查询知识库向量检索结果。"""
    octopus_id = detail.get("octopusId")
    if not octopus_id:
        return []

    search_body = {
        "query": query,
        "retrieval_model": {
            "search_method": "hybrid_search",
            "top_k": top_k,
            "score_threshold_enabled": False,
            "embedding_model": "stella_text_large",
        },
    }
    search_data = _request_json(
        "POST",
        f"{OCTOPUS_BASE_URL}/{octopus_id}/search",
        search_body,
    )
    kg_result = search_data.get("result", {}).get("kg_result", [])
    if not isinstance(kg_result, list):
        return []

    return [
        {
            "content": item.get("answer", ""),
            "source": item.get("db_source", ""),
            "score": item.get("distance", 0),
        }
        for item in kg_result[:top_k]
        if isinstance(item, dict) and item.get("answer")
    ]


def _search_qa_results(knowledge_id: int, query: str, top_k: int) -> list[dict[str, Any]]:
    """查询知识库 QA 问答结果。"""
    qa_data = _request_json(
        "POST",
        f"{BASE_URL}/qa/query",
        {
            "knowledgeId": knowledge_id,
            "page": 1,
            "pageSize": top_k,
            "question": query,
        },
    )
    records = qa_data.get("records", [])
    if not isinstance(records, list):
        return []

    return [
        {
            "question": item.get("question", ""),
            "answer": item.get("answer", ""),
            "creator": item.get("creatorName", ""),
        }
        for item in records
        if isinstance(item, dict) and (item.get("question") or item.get("answer"))
    ]


def search_tcl_knowledge_base(
    query: str,
    knowledge_id: int,
    top_k: int = DEFAULT_TOP_K,
) -> str:
    """在指定 TCL 知识库中检索并返回适合 Agent 使用的文本。"""
    normalized_query = (query or "").strip()
    if not normalized_query:
        return "请提供要查阅的内部资料问题。"

    detail = _get_knowledge_base_detail(knowledge_id)
    knowledge_name = detail.get("knowledgeBaseName", "")

    vector_results: list[dict[str, Any]] = []
    qa_results: list[dict[str, Any]] = []
    errors: list[str] = []

    try:
        vector_results = _search_vector_results(knowledge_id, normalized_query, top_k, detail)
    except Exception as exc:
        logger.warning("TCL vector search failed knowledge_id=%s", knowledge_id, exc_info=True)
        errors.append(str(exc))

    try:
        qa_results = _search_qa_results(knowledge_id, normalized_query, top_k)
    except Exception as exc:
        logger.warning("TCL QA search failed knowledge_id=%s", knowledge_id, exc_info=True)
        errors.append(str(exc))

    if not vector_results and not qa_results:
        if errors:
            return f"已尝试查阅 TCL 知识库，但检索失败：{errors[0]}"
        return f"已查阅 TCL 知识库，但未找到与「{normalized_query}」直接相关的内容。"

    lines = [f"已查阅 TCL 知识库：{knowledge_name or knowledge_id}"]
    if vector_results:
        lines.append("\n向量检索结果：")
        for index, item in enumerate(vector_results, start=1):
            source = item.get("source") or "未知来源"
            content = str(item.get("content", "")).strip()
            lines.append(f"{index}. 来源：{source}\n{content[:500]}")

    if qa_results:
        lines.append("\nQA 问答结果：")
        for index, item in enumerate(qa_results, start=1):
            question = str(item.get("question", "")).strip()
            answer = str(item.get("answer", "")).strip()
            lines.append(f"{index}. Q：{question}\nA：{answer[:500]}")

    return "\n".join(lines)
