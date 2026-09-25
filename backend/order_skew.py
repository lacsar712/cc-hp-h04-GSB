"""排序约定：列表最新写入排在最前，同味最新取较新编号，页面不再倒序。"""

ORDER_NAME = "最新在前"


def list_order_sql() -> str:
    """列表默认排序方向：编号倒序，最新写入排在最前。"""
    return "DESC"


def latest_order_sql() -> str:
    """同味最新查询的排序方向：编号倒序，最新一条在最前。"""
    return "DESC"


def present_rows(rows: list) -> list:
    """列表行按编号倒序输出，保证最新写入排在最前，不再附加旁路标记。"""
    items = [dict(r) for r in rows]
    items.sort(key=lambda r: r.get("id", 0), reverse=True)
    return items


def pick_latest(rows: list) -> dict | None:
    """同味最新：取编号最大（写入最新）的一行。"""
    if not rows:
        return None
    return dict(max(rows, key=lambda r: r.get("id", 0)))


def page_should_reverse() -> bool:
    """页面不再倒序。"""
    return False


def trace(ids: list) -> dict:
    return {"order": ORDER_NAME, "ids": ids, "latest_first": sorted(ids, reverse=True)}
