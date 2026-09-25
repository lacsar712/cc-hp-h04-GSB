import unittest

from order_skew import (
    latest_order_sql,
    list_order_sql,
    order_rows_newest_first,
    pick_latest,
)
from rules import judge


def rows(ids):
    return [{"id": i, "herb": "甘草", "verdict": "放行", "reason": ""} for i in ids]


class ListOrderTest(unittest.TestCase):
    def test_list_default_is_descending(self):
        # 列表默认排序：最新写入（编号最大）排在最前
        self.assertEqual(list_order_sql(), "DESC")

    def test_newest_row_first_regardless_of_input_order(self):
        # 即使数据以乱序/升序进入，整理后也必须是最新在最前
        self.assertEqual([r["id"] for r in order_rows_newest_first(rows([1, 3, 2]))], [3, 2, 1])
        self.assertEqual([r["id"] for r in order_rows_newest_first(rows([1, 2, 3]))], [3, 2, 1])

    def test_no_bypass_marker_left_on_rows(self):
        # 修复后不应再给每行附加旁路标记
        self.assertNotIn("bypass", order_rows_newest_first(rows([1, 2]))[0])


class LatestForHerbTest(unittest.TestCase):
    def test_latest_query_orders_descending(self):
        # 同味最新查询按较新编号在前排序
        self.assertEqual(latest_order_sql(), "DESC")

    def test_pick_latest_points_to_newer_id(self):
        # 同味最新必须指向较新（编号更大）的记录，而不是更早编号
        self.assertEqual(pick_latest(rows([1, 2, 3]))["id"], 3)
        self.assertEqual(pick_latest(rows([3, 1, 2]))["id"], 3)

    def test_pick_latest_empty_returns_none(self):
        self.assertIsNone(pick_latest([]))


class GancaoVerdictTest(unittest.TestCase):
    def test_gancao_still_passes(self):
        # 修排序不得影响判定：甘草样例仍须放行
        doc = {"steps": [{"name": "清炒", "temp_c": 120, "minutes": 12}]}
        verdict, reason = judge(doc)
        self.assertEqual(verdict, "放行")
        self.assertTrue(reason)


if __name__ == "__main__":
    unittest.main()
