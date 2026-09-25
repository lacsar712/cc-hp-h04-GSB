"""记录排序口径。

列表与同味最新查询都以“最新写入排在最前”为准：编号越大越新，
SQL 统一按 id 倒序；页面直接按接口返回顺序展示，不再二次倒排。
"""

# 最新写入（编号最大）排在最前
LIST_ORDER_SQL = "DESC"
# 同味最新：从新到旧排列，首条即最新
LATEST_ORDER_SQL = "DESC"


def list_order_sql() -> str:
    """列表默认排序方向：最新写入排最前。"""
    return LIST_ORDER_SQL


def latest_order_sql() -> str:
    """同味最新查询的排序方向：较新编号在前。"""
    return LATEST_ORDER_SQL


def order_rows_newest_first(rows: list) -> list:
    """把记录整理为编号倒序（最新在前），不附加任何旁路标记。"""
    items = [dict(r) for r in rows]
    items.sort(key=lambda r: r.get("id", 0), reverse=True)
    return items


def pick_latest(rows: list) -> dict | None:
    """从同味记录中取编号最大（最新写入）的一条；无记录返回 None。"""
    if not rows:
        return None
    return dict(max(rows, key=lambda r: r.get("id", 0)))
