import io
from unittest import TestCase
from unittest.mock import patch
from Elia.accounting.readRecord import ViewRecordPage, ViewRecordOption
from mock_db import MockDB
import sys

class TestViewRecord(MockDB):
    def setUp(self) -> None:
        self.viewPage = ViewRecordPage()
    
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_show(self, _stdout):
        self.viewPage.show()
        output_lines = _stdout.getvalue().strip().split("\n")
        self.assertEqual(output_lines[0], "%d: 查看本日紀錄" % ViewRecordOption.TODAY)
        self.assertEqual(output_lines[1], "%d: 查看本週紀錄" % ViewRecordOption.WEEK)
        self.assertEqual(output_lines[2], "%d: 查看本月紀錄" % ViewRecordOption.MONTH)
        self.assertEqual(output_lines[3], "%d: 查看指定時間紀錄" % ViewRecordOption.OTHER)
        self.assertEqual(output_lines[4], "%d: 回到上一頁" % ViewRecordOption.BACK)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["0", "6", "F", "1", "2", "3", "4", "5"])
    def test_choose(self, _input, _stdout):
        self.assertEqual(self.viewPage.choose(), 1)
        self.assertEqual(_input.call_count, 4)
        self.assertEqual(_stdout.getvalue(), "請輸入 1 到 5 之間的數字:\n" * 3)
        self.assertEqual(self.viewPage.choose(), 2)
        self.assertEqual(_input.call_count, 5)
        self.assertEqual(self.viewPage.choose(), 3)
        self.assertEqual(_input.call_count, 6)
        self.assertEqual(self.viewPage.choose(), 4)
        self.assertEqual(_input.call_count, 7)
        self.assertEqual(self.viewPage.choose(), 5)
        self.assertEqual(_input.call_count, 8)
    

    @patch.object(ViewRecordPage, "viewToday")
    @patch.object(ViewRecordPage, "viewWeek")
    @patch.object(ViewRecordPage, "viewMonth")
    @patch.object(ViewRecordPage, "viewOther")
    def test_execute(self, _viewOther, _viewMonth, _viewWeek, _viewToday):
        self.viewPage.execute(ViewRecordOption.OTHER)
        self.assertEqual(_viewOther.call_count, 1)
        self.viewPage.execute(ViewRecordOption.MONTH)
        self.assertEqual(_viewMonth.call_count, 1)
        self.viewPage.execute(ViewRecordOption.WEEK)
        self.assertEqual(_viewWeek.call_count, 1)
        self.viewPage.execute(ViewRecordOption.TODAY)
        self.assertEqual(_viewToday.call_count, 1)


    @patch.object(ViewRecordPage, "execute")
    @patch.object(
        ViewRecordPage,
        "choose",
        side_effect=[ViewRecordOption.TODAY, ViewRecordOption.WEEK, ViewRecordOption.MONTH, ViewRecordOption.OTHER, ViewRecordOption.BACK],
    )
    @patch.object(ViewRecordPage, "show")
    def test_start(self, _show, _choose, _execute):
        self.viewPage.start()
        self.assertEqual(_show.call_count, 5)
        self.assertEqual(_choose.call_count, 5)
        self.assertEqual(_execute.call_count, 4)