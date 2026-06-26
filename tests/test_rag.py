from pathlib import Path

from services.rag_service import SUPPORTED_SUFFIXES, _read_document_text, search_internal_docs
from tools.rag_tool import query_internal_docs


def test_supported_internal_doc_formats():
    assert {".md", ".txt", ".pdf", ".docx"}.issubset(SUPPORTED_SUFFIXES)


def test_read_plain_text_internal_doc(tmp_path):
    doc_path = tmp_path / "制度.txt"
    doc_path.write_text("测试制度内容", encoding="utf-8")

    assert _read_document_text(Path(doc_path)) == "测试制度内容"


def test_search_internal_docs_from_employee_handbook():
    result = search_internal_docs("报销多久能到账")

    assert "已查阅内部资料" in result
    assert "报销流程说明.md" in result or "员工手册.md" in result
    assert "5 个工作日" in result or "报销" in result


def test_search_internal_docs_attendance_policy():
    result = search_internal_docs("怎么打卡")

    assert "已查阅内部资料" in result
    assert "考勤与打卡制度.md" in result or "员工手册.md" in result
    assert "打卡" in result or "补卡" in result


def test_search_internal_docs_reimbursement_policy():
    result = search_internal_docs("报销需要什么发票")

    assert "已查阅内部资料" in result
    assert "报销流程说明.md" in result
    assert "发票" in result or "支付凭证" in result


def test_search_internal_docs_ai_security_policy():
    result = search_internal_docs("可以使用 AI 工具处理客户资料吗")

    assert "已查阅内部资料" in result
    assert "信息安全与AI使用规范.md" in result
    assert "客户隐私" in result or "脱敏" in result or "敏感" in result


def test_search_internal_docs_available_scope():
    result = search_internal_docs("你可以查什么内部资料呢")

    assert "已查阅内部资料" in result
    assert "员工手册.md" in result
    assert "考勤与打卡制度.md" in result
    assert "报销流程说明.md" in result
    assert "信息安全与AI使用规范.md" in result


def test_search_internal_docs_no_match():
    result = search_internal_docs("火星基地停车规则")

    assert "已查阅内部资料" in result
    assert "未找到" in result


def test_query_internal_docs_empty_query():
    result = query_internal_docs.invoke({"query": ""})

    assert "请说明" in result
