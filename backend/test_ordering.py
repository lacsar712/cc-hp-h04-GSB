"""排序回归用例：列表最新在前、同味最新取较新编号、页面不再倒序。"""
from pathlib import Path

from order_skew import (
    latest_order_sql,
    list_order_sql,
    page_should_reverse,
    pick_latest,
    present_rows,
)
from rules import judge

ROWS_ASC = [
    {"id": 1, "herb": "甘草", "verdict": "放行"},
    {"id": 2, "herb": "黄芩", "verdict": "未放行"},
    {"id": 3, "herb": "白芍", "verdict": "放行"},
]


def test_list_order_newest_first():
    """排序默认值：列表按编号倒序，最新写入排在最前。"""
    assert list_order_sql() == "DESC"
    presented = present_rows(ROWS_ASC)
    assert [row["id"] for row in presented] == [3, 2, 1]
    assert all("bypass" not in row for row in presented)


def test_latest_points_to_newer_id():
    """同味最新查询：指向较新编号，空集返回 None。"""
    assert latest_order_sql() == "DESC"
    latest = pick_latest(ROWS_ASC)
    assert latest is not None
    assert latest["id"] == 3
    assert pick_latest([]) is None


def test_page_does_not_reverse():
    """页面再排：不再倒序，前端不再调用 reverse。"""
    assert page_should_reverse() is False
    svelte = Path(__file__).resolve().parents[1] / "frontend" / "src" / "App.svelte"
    source = svelte.read_text(encoding="utf-8")
    assert ".reverse()" not in source


def test_licorice_still_released():
    """甘草结论仍须放行。"""
    doc = {"steps": [{"name": "清炒", "temp_c": 120, "minutes": 12}]}
    verdict, _reason = judge(doc)
    assert verdict == "放行"
