import io
from unittest import TestCase
from unittest.mock import patch
from readRecord import ReadRecordPage, ReadRecordOption
from mock_db import MockDB
from accessor import ExecutionStatus as es
import const

class TestReadRecord(MockDB):
    # def setUp(self) -> None:
    #     self.viewPage = ReadRecordPage()
    
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_show(self, _stdout):
        ReadRecordPage.show()
        output_lines = _stdout.getvalue().strip().split("\n")
        self.assertEqual(output_lines[0], "%d: 查看本日紀錄" % ReadRecordOption.TODAY)
        self.assertEqual(output_lines[1], "%d: 查看本週紀錄" % ReadRecordOption.WEEK)
        self.assertEqual(output_lines[2], "%d: 查看本月紀錄" % ReadRecordOption.MONTH)
        self.assertEqual(output_lines[3], "%d: 查看指定時間紀錄" % ReadRecordOption.OTHER)
        self.assertEqual(output_lines[4], "%d: 回到上一頁" % ReadRecordOption.BACK)

    
    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_show(self, _stdout):
    #     ReadRecordPage.show()
    #     output_lines = _stdout.getvalue().strip().split('\n')
    #     self.assertEqual(output_lines[0], "%d: 新增支付方式" % PaymentOption.CREATE)
    #     self.assertEqual(output_lines[1], "%d: 查看支付方式" % PaymentOption.READ)
    #     self.assertEqual(output_lines[2], "%d: 修改支付方式" % PaymentOption.UPDATE)
    #     self.assertEqual(output_lines[3], "%d: 刪除支付方式" % PaymentOption.DELETE)
    #     self.assertEqual(output_lines[4], "%d: 回到上一頁" % PaymentOption.BACK)
    

    # @patch("sys.stdout", new_callable=io.StringIO)
    # @patch("builtins.input", side_effect=["0", "6", "F", "1", "2", "3", "4", "5"])
    # def test_choose(self, _input, _stdout):
    #     self.assertEqual(self.viewPage.choose(), 1)
    #     self.assertEqual(_input.call_count, 4)
    #     self.assertEqual(_stdout.getvalue(), "請輸入 1 到 5 之間的數字:\n" * 3)
    #     self.assertEqual(self.viewPage.choose(), 2)
    #     self.assertEqual(_input.call_count, 5)
    #     self.assertEqual(self.viewPage.choose(), 3)
    #     self.assertEqual(_input.call_count, 6)
    #     self.assertEqual(self.viewPage.choose(), 4)
    #     self.assertEqual(_input.call_count, 7)
    #     self.assertEqual(self.viewPage.choose(), 5)
    #     self.assertEqual(_input.call_count, 8)
    

    # @patch.object(ReadRecordPage, "viewToday")
    # @patch.object(ReadRecordPage, "viewWeek")
    # @patch.object(ReadRecordPage, "viewMonth")
    # @patch.object(ReadRecordPage, "viewOther")
    # def test_execute(self, _viewOther, _viewMonth, _viewWeek, _viewToday):
    #     self.viewPage.execute(ReadRecordOption.OTHER)
    #     self.assertEqual(_viewOther.call_count, 1)
    #     self.viewPage.execute(ReadRecordOption.MONTH)
    #     self.assertEqual(_viewMonth.call_count, 1)
    #     self.viewPage.execute(ReadRecordOption.WEEK)
    #     self.assertEqual(_viewWeek.call_count, 1)
    #     self.viewPage.execute(ReadRecordOption.TODAY)
    #     self.assertEqual(_viewToday.call_count, 1)


    # @patch.object(ReadRecordPage, "execute")
    # @patch.object(
    #     ReadRecordPage,
    #     "choose",
    #     side_effect=[ReadRecordOption.TODAY, ReadRecordOption.WEEK, ReadRecordOption.MONTH, ReadRecordOption.OTHER, ReadRecordOption.BACK],
    # )
    # @patch.object(ReadRecordPage, "show")
    # def test_start(self, _show, _choose, _execute):
    #     self.viewPage.start()
    #     self.assertEqual(_show.call_count, 5)
    #     self.assertEqual(_choose.call_count, 5)
    #     self.assertEqual(_execute.call_count, 4)