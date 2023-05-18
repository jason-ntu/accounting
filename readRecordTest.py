import io
from unittest import TestCase
from unittest.mock import patch
from readRecord import ReadRecordPage, ReadRecordOption
from mock_db import MockDB
from accessor import ExecutionStatus as es
import const
from datetime import datetime

class TestReadRecord(MockDB):
    
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_show(self, _stdout):
        ReadRecordPage.show()
        output_lines = _stdout.getvalue().strip().split("\n")
        self.assertEqual(output_lines[0], "%d: 查看本日紀錄" % ReadRecordOption.TODAY)
        self.assertEqual(output_lines[1], "%d: 查看本週紀錄" % ReadRecordOption.WEEK)
        self.assertEqual(output_lines[2], "%d: 查看本月紀錄" % ReadRecordOption.MONTH)
        self.assertEqual(output_lines[3], "%d: 查看指定時間紀錄" % ReadRecordOption.OTHER)
        self.assertEqual(output_lines[4], "%d: 回到上一頁" % ReadRecordOption.BACK)
    
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_hints(self, _stdout):
        hints = [(ReadRecordPage.hintGetStartDate, "請輸入 開始 時間(yyyy-mm-dd): \n"),
                 (ReadRecordPage.hintGetEndDate, "請輸入 結束 時間(yyyy-mm-dd): \n")]
        for hint in hints:
            hint[0]()
            self.assertMultiLineEqual(_stdout.getvalue(), hint[1])
            _stdout.truncate(0)
            _stdout.seek(0)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["0", "6", "F", "1", "2", "3", "4", "5"])
    def test_choose(self, _input, _stdout):
        self.assertEqual(ReadRecordPage.choose(), 1)
        self.assertEqual(_input.call_count, 4)
        self.assertEqual(ReadRecordPage.choose(), 2)
        self.assertEqual(_input.call_count, 5)
        self.assertEqual(ReadRecordPage.choose(), 3)
        self.assertEqual(_input.call_count, 6)
        self.assertEqual(ReadRecordPage.choose(), 4)
        self.assertEqual(_input.call_count, 7)
        self.assertEqual(ReadRecordPage.choose(), 5)
        self.assertEqual(_input.call_count, 8)
        self.assertEqual(_stdout.getvalue(), "請輸入 1 到 5 之間的數字:\n" * 3)

    @patch.object(ReadRecordPage, "viewToday")
    @patch.object(ReadRecordPage, "viewWeek")
    @patch.object(ReadRecordPage, "viewMonth")
    @patch.object(ReadRecordPage, "viewOther")
    def test_execute(self, _viewOther, _viewMonth, _viewWeek, _viewToday):
        ReadRecordPage.execute(ReadRecordOption.OTHER)
        self.assertEqual(_viewOther.call_count, 1)
        ReadRecordPage.execute(ReadRecordOption.MONTH)
        self.assertEqual(_viewMonth.call_count, 1)
        ReadRecordPage.execute(ReadRecordOption.WEEK)
        self.assertEqual(_viewWeek.call_count, 1)
        ReadRecordPage.execute(ReadRecordOption.TODAY)
        self.assertEqual(_viewToday.call_count, 1)
    
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_viewToday(self, _stdout):
        with self.mock_db_config:
            ReadRecordPage.setUp_connection_and_table()
            ReadRecordPage.viewToday()
            ReadRecordPage.tearDown_connection(es.NONE)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "1  類別: FOOD  金額: 50  支付方式: 現金  地點: 7-11  時間: " + str(datetime.today().date()))
        self.assertEqual(output_lines[1], "2  類別: BEVERAGE  金額: 100  支付方式: 現金  地點: comebuy  時間: " + str(datetime.today().date()))

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_viewWeek(self, _stdout):
        with self.mock_db_config:
            ReadRecordPage.setUp_connection_and_table()
            ReadRecordPage.viewWeek()
            ReadRecordPage.tearDown_connection(es.NONE)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "1  類別: FOOD  金額: 50  支付方式: 現金  地點: 7-11  時間: " + str(datetime.today().date()))
        self.assertEqual(output_lines[1], "2  類別: BEVERAGE  金額: 100  支付方式: 現金  地點: comebuy  時間: " + str(datetime.today().date()))
        self.assertEqual(output_lines[2], "3  類別: BEVERAGE  金額: 150  支付方式: 現金  地點: 茶湯會  時間: " + "2023-05-17")

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_viewMonth(self, _stdout):
        with self.mock_db_config:
            ReadRecordPage.setUp_connection_and_table()
            ReadRecordPage.viewMonth()
            ReadRecordPage.tearDown_connection(es.NONE)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "1  類別: FOOD  金額: 50  支付方式: 現金  地點: 7-11  時間: " + str(datetime.today().date()))
        self.assertEqual(output_lines[1], "2  類別: BEVERAGE  金額: 100  支付方式: 現金  地點: comebuy  時間: " + str(datetime.today().date()))
        self.assertEqual(output_lines[2], "3  類別: BEVERAGE  金額: 150  支付方式: 現金  地點: 茶湯會  時間: " + "2023-05-17")
        self.assertEqual(output_lines[3], "4  類別: FOOD  金額: 80  支付方式: 現金  地點: FamilyMart  時間: " + "2023-05-25")

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["2023-05-17", "2023-05-26"])
    def test_viewOther(self, _input, _stdout):
        with self.mock_db_config:
            ReadRecordPage.setUp_connection_and_table()
            ReadRecordPage.viewOther()
            ReadRecordPage.tearDown_connection(es.NONE)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "請輸入 開始 時間(yyyy-mm-dd): ")
        self.assertEqual(output_lines[1], "請輸入 結束 時間(yyyy-mm-dd): ")
        self.assertEqual(output_lines[2], "1  類別: FOOD  金額: 50  支付方式: 現金  地點: 7-11  時間: 2023-05-18")
        self.assertEqual(output_lines[3], "2  類別: BEVERAGE  金額: 100  支付方式: 現金  地點: comebuy  時間: 2023-05-18")
        self.assertEqual(output_lines[4], "3  類別: BEVERAGE  金額: 150  支付方式: 現金  地點: 茶湯會  時間: 2023-05-17")
        self.assertEqual(output_lines[5], "4  類別: FOOD  金額: 80  支付方式: 現金  地點: FamilyMart  時間: 2023-05-25")

    @patch.object(ReadRecordPage, "execute")
    @patch.object(ReadRecordPage, "choose",
        side_effect=[ReadRecordOption.TODAY, ReadRecordOption.WEEK, ReadRecordOption.MONTH, ReadRecordOption.OTHER, ReadRecordOption.BACK],
    )
    @patch.object(ReadRecordPage, "show")
    def test_start(self, _show, _choose, _execute):
        ReadRecordPage.start()
        self.assertEqual(_show.call_count, 5)
        self.assertEqual(_choose.call_count, 5)
        self.assertEqual(_execute.call_count, 4)