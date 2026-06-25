"""内部资料本地检索服务。"""

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

DOCS_DIR = Path(__file__).resolve().parents[1] / "data" / "internal_docs"
SUPPORTED_SUFFIXES = {".md", ".txt"}
MAX_RESULTS = 3
MAX_SNIPPET_LENGTH = 360


def _load_documents() -> list[dict]:
    """读取本地内部资料文档。"""
    if not DOCS_DIR.exists():
        return []

    docs = []
    for path in DOCS_DIR.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8").strip()
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8-sig", errors="ignore").strip()
        except OSError:
            logger.exception("internal doc read failed path=%s", path.name)
            continue
        if text:
            docs.append({"source": path.name, "text": text})
    return docs


def _split_chunks(text: str) -> list[str]:
    """按标题和空行切分文档片段。"""
    chunks = []
    current = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            if current:
                chunks.append("\n".join(current).strip())
                current = []
            continue
        if stripped.startswith("#") and current:
            chunks.append("\n".join(current).strip())
            current = [stripped]
        else:
            current.append(stripped)
    if current:
        chunks.append("\n".join(current).strip())
    return [chunk for chunk in chunks if chunk]


def _query_terms(query: str) -> list[str]:
    """提取中英文关键词。"""
    normalized = query.strip().lower()
    terms = re.findall(r"[\u4e00-\u9fff]{2,}|[a-zA-Z0-9]{2,}", normalized)
    aliases = {
        "请假": ["年假", "病假", "事假", "审批"],
        "请假制度": ["请假", "年假", "病假", "事假", "审批"],
        "报销": ["费用", "发票", "财务", "差旅"],
        "报销制度": ["报销", "费用", "发票", "财务", "差旅"],
        "打卡": ["考勤", "补卡", "迟到"],
        "打卡制度": ["打卡", "考勤", "补卡", "迟到", "早退"],
        "考勤": ["打卡", "补卡", "迟到", "早退", "出勤"],
        "考勤制度": ["考勤", "打卡", "补卡", "迟到", "早退", "出勤"],
        "居家": ["远程", "居家办公"],
        "居家办公": ["居家", "远程", "线上会议"],
        "内部资料": ["员工手册", "公司制度", "考勤", "请假", "报销", "信息安全"],
        "员工手册": ["工作时间", "考勤", "请假", "报销", "居家办公", "信息安全", "绩效", "培训", "离职"],
        "ai": ["AI", "信息安全", "敏感"],
    }
    expanded = list(terms)
    for term in terms:
        expanded.extend(aliases.get(term, []))
    for key, values in aliases.items():
        if key in normalized:
            expanded.append(key)
            expanded.extend(values)
    return list(dict.fromkeys(expanded))


def _score_chunk(chunk: str, terms: list[str]) -> int:
    """按关键词命中次数计算简单相关性分数。"""
    chunk_lower = chunk.lower()
    return sum(chunk_lower.count(term.lower()) for term in terms)


def _shorten(text: str) -> str:
    """限制返回片段长度。"""
    clean = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(clean) <= MAX_SNIPPET_LENGTH:
        return clean
    return clean[:MAX_SNIPPET_LENGTH].rstrip() + "…"


def _is_scope_query(query: str) -> bool:
    """判断用户是否在询问内部资料范围。"""
    return any(
        phrase in query
        for phrase in ("可以查什么", "能查什么", "有什么内部资料", "内部资料有哪些", "文档库有什么")
    )


def _format_available_scope(docs: list[dict]) -> str:
    """返回当前本地知识库可查询范围。"""
    lines = ["已查阅内部资料，当前本地知识库可查询以下资料："]
    for doc in docs:
        headings = [
            line.lstrip("#").strip()
            for line in doc["text"].splitlines()
            if line.startswith("## ")
        ]
        lines.append(f"\n- 来源：{doc['source']}")
        if headings:
            lines.append("  可查章节：" + "、".join(headings[:12]))
    return "\n".join(lines)


def search_internal_docs(query: str) -> str:
    """搜索内部文档知识库。"""
    normalized_query = (query or "").strip()
    if not normalized_query:
        return "请提供要查阅的内部资料问题，例如：请假流程、报销标准、信息安全要求。"

    docs = _load_documents()
    if not docs:
        return "未找到可查阅的内部资料。请先将 .md 或 .txt 文档放入 data/internal_docs/。"

    if _is_scope_query(normalized_query):
        return _format_available_scope(docs)

    terms = _query_terms(normalized_query)
    scored_chunks = []
    for doc in docs:
        for chunk in _split_chunks(doc["text"]):
            score = _score_chunk(chunk, terms)
            if score > 0:
                scored_chunks.append((score, doc["source"], chunk))

    if not scored_chunks:
        return f"已查阅内部资料，但未找到与「{normalized_query}」直接相关的内容。"

    scored_chunks.sort(key=lambda item: item[0], reverse=True)
    results = scored_chunks[:MAX_RESULTS]
    lines = ["已查阅内部资料，找到以下相关内容："]
    for index, (_, source, chunk) in enumerate(results, start=1):
        lines.append(f"\n{index}. 来源：{source}\n{_shorten(chunk)}")
    return "\n".join(lines)
