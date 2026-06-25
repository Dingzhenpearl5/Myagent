from services.rag_service import search_internal_docs
from tools.rag_tool import query_internal_docs


def test_search_internal_docs_from_employee_handbook():
    result = search_internal_docs("报销多久能到账")

    assert "已查阅内部资料" in result
    assert "员工手册.md" in result
    assert "5 个工作日" in result or "报销" in result


def test_search_internal_docs_attendance_policy():
    result = search_internal_docs("打卡制度")

    assert "已查阅内部资料" in result
    assert "员工手册.md" in result
    assert "考勤" in result or "补卡" in result


def test_search_internal_docs_available_scope():
    result = search_internal_docs("你可以查什么内部资料呢")

    assert "已查阅内部资料" in result
    assert "员工手册.md" in result
    assert "请假" in result or "报销" in result or "信息安全" in result


def test_search_internal_docs_no_match():
    result = search_internal_docs("火星基地停车规则")

    assert "已查阅内部资料" in result
    assert "未找到" in result


def test_query_internal_docs_empty_query():
    result = query_internal_docs.invoke({"query": ""})

    assert "请说明" in result
