from io import StringIO
from unittest import TestCase
from unittest.mock import patch
from report import ReportPage, ReportOption
from datetime import datetime
from mock_db import MockDB

class TestReport(TestCase):
    def setUp(self) -> None:
        self.reportPage = ReportPage()

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', side_effect=['0', '3', 'F', '1', '2'])
    def test_choose(self, _input, _stdout):
        self.assertEqual(self.reportPage.choose(), 1)
        self.assertEqual(_input.call_count, 4)
        self.assertEqual(_stdout.getvalue(), "請輸入 1 到 2 之間的數字:\n"*3)
        self.assertEqual(self.reportPage.choose(), 2)
        self.assertEqual(_input.call_count, 5)


    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', side_effect=['2022/01/10', '2023/01/10'])
    @patch.object(ReportPage, 'Report')
    def test_chooseInterval_with_valid_input(self, _report, _input, _stdout):
        self.reportPage.chooseInterval()
        self.assertEqual(_input.call_count, 2)
        self.assertEqual(_report.call_count, 1)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', side_effect=['2022/02/30', '2023/01/01', '2022/01/01', '2022/13/10'])
    def test_chooseInterval_with_invalid_date(self, _input, _stdout):
        self.reportPage.chooseInterval()
        self.assertIn('日期格式錯誤', _stdout.getvalue())
        _stdout.truncate(0)
        _stdout.seek(0)
        self.reportPage.chooseInterval()
        self.assertEqual(_input.call_count, 4)
        self.assertIn('日期格式錯誤', _stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', side_effect=['2022/01/10', '2022/01/10','2022/12/31', '2021/12/31'])
    def test_chooseInterval_invaild_internal(self, _input, _stdout):
        self.reportPage.chooseInterval()
        self.assertIn('Error: 時間區間至少一天',_stdout.getvalue())
        _stdout.truncate(0)
        _stdout.seek(0)
        self.reportPage.chooseInterval()
        self.assertIn('Error: 時間區間至少一天',_stdout.getvalue())

    @patch.object(ReportPage, 'Report')
    def test_Report(self, _report):
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2022, 1, 10)
        self.reportPage.Report(start_date, end_date)
        _report.assert_called_once_with(start_date, end_date)

    # 各項比例加總=100%
    def test_checkTotalProportion(self):
        pass

    # 每一個數字都是非負
    def test_checkNonnegative(self):
        pass