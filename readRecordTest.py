import io
from unittest import TestCase
from unittest.mock import patch
from readRecord import ReadRecordPage, ReadRecordOption
from mock_db import MockDB
from accessor import ExecutionStatus as es
import const
from datetime import datetime
from freezegun import freeze_time

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
        hints = [(ReadRecordPage.hintGetStartDate, "請輸入 開始 時間(yyyy-mm-dd):\n"),
                 (ReadRecordPage.hintGetEndDate, "請輸入 結束 時間(yyyy-mm-dd):\n")]
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
    @freeze_time("2023-05-18")
    def test_viewToday(self, _stdout):
        with self.mock_db_config:
            ReadRecordPage.setUp_connection_and_table()
            ReadRecordPage.viewToday()
            ReadRecordPage.tearDown_connection(es.NONE)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(len(output_lines), 1)
        self.assertEqual(output_lines[0], "2 EXPENSE  類別: 住宿  金額: 2500.0  帳戶: Line Pay  地點: 其它  消費時間: 2023-05-18  扣款時間: 2023-05-18  發票號碼:   備註: taipei")

        
    @patch("sys.stdout", new_callable=io.StringIO)
    @freeze_time("2023-05-18")
    def test_viewWeek(self, _stdout):
        with self.mock_db_config:
            ReadRecordPage.setUp_connection_and_table()
            ReadRecordPage.viewWeek()
            ReadRecordPage.tearDown_connection(es.NONE)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(len(output_lines), 2)
        self.assertEqual(output_lines[0], "2 EXPENSE  類別: 住宿  金額: 2500.0  帳戶: Line Pay  地點: 其它  消費時間: 2023-05-18  扣款時間: 2023-05-18  發票號碼:   備註: taipei")
        self.assertEqual(output_lines[1], "4 EXPENSE  類別: 飲料  金額: 100.0  帳戶: Line Pay  地點: 飲料店  消費時間: 2023-05-19  扣款時間: 2023-05-19  發票號碼:   備註: 麻古-芝芝芒果")
        
    @patch("sys.stdout", new_callable=io.StringIO)
    @freeze_time("2023-05-18")
    def test_viewMonth(self, _stdout):
        with self.mock_db_config:
            ReadRecordPage.setUp_connection_and_table()
            ReadRecordPage.viewMonth()
            ReadRecordPage.tearDown_connection(es.NONE)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(len(output_lines), 4)
        self.assertEqual(output_lines[0], "1 EXPENSE  類別: 食物  金額: 50.0  帳戶: 現金  地點: 便利商店  消費時間: 2023-05-01  扣款時間: 2023-05-01  發票號碼: 12345678  備註: milk")
        self.assertEqual(output_lines[1], "2 EXPENSE  類別: 住宿  金額: 2500.0  帳戶: Line Pay  地點: 其它  消費時間: 2023-05-18  扣款時間: 2023-05-18  發票號碼:   備註: taipei")
        self.assertEqual(output_lines[2], "3 INCOME  類別: 其它  金額: 10000.0  帳戶: 中華郵政  地點: 其它  消費時間: 2023-05-22  扣款時間: 2023-05-23  發票號碼: 19970901  備註: ")
        self.assertEqual(output_lines[3], "4 EXPENSE  類別: 飲料  金額: 100.0  帳戶: Line Pay  地點: 飲料店  消費時間: 2023-05-19  扣款時間: 2023-05-19  發票號碼:   備註: 麻古-芝芝芒果")


    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["2023-05-01", "2023-05-18"])
    @freeze_time("2023-05-18")
    def test_viewOther(self, _input, _stdout):
        with self.mock_db_config:
            ReadRecordPage.setUp_connection_and_table()
            ReadRecordPage.viewOther()
            ReadRecordPage.tearDown_connection(es.NONE)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(len(output_lines), 4)
        self.assertEqual(output_lines[0], "請輸入 開始 時間(yyyy-mm-dd):")
        self.assertEqual(output_lines[1], "請輸入 結束 時間(yyyy-mm-dd):")
        self.assertEqual(output_lines[2], "1 EXPENSE  類別: 食物  金額: 50.0  帳戶: 現金  地點: 便利商店  消費時間: 2023-05-01  扣款時間: 2023-05-01  發票號碼: 12345678  備註: milk")
        self.assertEqual(output_lines[3], "2 EXPENSE  類別: 住宿  金額: 2500.0  帳戶: Line Pay  地點: 其它  消費時間: 2023-05-18  扣款時間: 2023-05-18  發票號碼:   備註: taipei")

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