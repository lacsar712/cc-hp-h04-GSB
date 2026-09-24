"""排序颠倒旁路：列表升序、同味最新取最旧、页面再倒序。"""

BYPASS_NAME = "排序颠倒旁路"


def list_order_sql() -> str:
    return "ASC"


def latest_order_sql() -> str:
    return "ASC"


def skew_rows(rows: list) -> list:
    items = [dict(r) for r in rows]
    items.sort(key=lambda r: r.get("id", 0))
    for item in items:
        item["bypass"] = BYPASS_NAME
    return items


def pick_latest(rows: list) -> dict | None:
    if not rows:
        return None
    return dict(sorted(rows, key=lambda r: r.get("id", 0))[0])


def page_should_reverse() -> bool:
    return True


def trace(ids: list) -> dict:
    return {"bypass": BYPASS_NAME, "ids": ids, "reversed": list(reversed(ids))}
