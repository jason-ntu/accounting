import io
from unittest.mock import patch
from report import ReportPage, ReportOption, ReportByOption
from mock_db import MockDB
from accessor import ExecutionStatus as es
import const
from IEDirection import IEDirection

class TestReport(MockDB):

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_show(self, _stdout):
        ReportPage.show()
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "%d: 選擇欲查詢的區間" % ReportOption.CHOOSE)
        self.assertEqual(output_lines[1], "%d: 回到上一頁" % ReportOption.BACK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_hints(self, _stdout):
        hints = [(ReportPage.hint_start_date, "請輸入\"起始\"日期 (yyyy-mm-dd):\n"),
                 (ReportPage.hint_finish_date, "請輸入\"結束\"日期 (yyyy-mm-dd):\n"),
                 (ReportPage.hint_choose_report_IE, "查看(1 收入, 2 支出):\n"),
                 (ReportPage.hint_choose_report_type, "報表顯示類型(1 依\"類別\" 2 \"依支付方式\"):\n")]
        for hint in hints:
            hint[0]()
            self.assertMultiLineEqual(_stdout.getvalue(), hint[1])
            _stdout.truncate(0)
            _stdout.seek(0)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['0', '3', 'F', '1', '2'])
    def test_choose(self, _input, _stdout):
        self.assertEqual(ReportPage.choose(), 1)
        self.assertEqual(_input.call_count, 4)
        self.assertEqual(_stdout.getvalue(), "請輸入 1 到 2 之間的數字:\n"*3)
        self.assertEqual(ReportPage.choose(), 2)
        self.assertEqual(_input.call_count, 5)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(ReportPage, 'chooseInterval')
    def test_execute(self, _chooseInterval, _stdout):
        with self.mock_db_config:
            _chooseInterval.return_value = False
            ReportPage.execute(ReportOption.CHOOSE)
            self.assertEqual(_chooseInterval.call_count, 1)

            _chooseInterval.return_value = True
            ReportPage.execute(ReportOption.CHOOSE)
            self.assertEqual(_chooseInterval.call_count, 2)

            ReportPage.execute(ReportOption.BACK)
            self.assertEqual(_chooseInterval.call_count, 3)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "%s操作失敗%s" %
                         (const.ANSI_RED, const.ANSI_RESET))
        self.assertEqual(output_lines[1], "%s操作成功%s" %
                         (const.ANSI_GREEN, const.ANSI_RESET))
        self.assertEqual(output_lines[2], "%s操作成功%s" %
                         (const.ANSI_GREEN, const.ANSI_RESET))

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['2022-01-10', '2023-01-10'])
    @patch.object(ReportPage, 'hint_finish_date')
    @patch.object(ReportPage, 'hint_start_date')
    @patch.object(ReportPage, 'chooseReportIE')
    def test_chooseInterval_with_valid_input(self, _chooseReportIE, _hint_start_date, _hint_finish_date, _input, _stdout):
        ReportPage.chooseInterval()
        self.assertEqual(_stdout.getvalue().strip(), "起始日期 00:00:00 到結束日期 23:59:59")
        self.assertEqual(_input.call_count, 2)
        self.assertEqual(_chooseReportIE.call_count, 1)
        self.assertEqual(_hint_start_date.call_count, 1)
        self.assertEqual(_hint_finish_date.call_count, 1)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['2022-02-30', '2023-0-01', '2022-01-01', '2022-13-10'])
    def test_chooseInterval_with_invalid_date(self, _input, _stdout):
        ReportPage.chooseInterval()
        self.assertIn('日期格式錯誤', _stdout.getvalue())
        _stdout.truncate(0)
        _stdout.seek(0)
        ReportPage.chooseInterval()
        self.assertEqual(_input.call_count, 4)
        self.assertIn('日期格式錯誤', _stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['2022-01-10', '2022-01-09'])
    def test_chooseInterval_invaild_internal(self, _input, _stdout):
        ReportPage.chooseInterval()
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "起始日期 00:00:00 到結束日期 23:59:59")
        self.assertEqual(output_lines[1], "請輸入\"起始\"日期 (yyyy-mm-dd):")
        self.assertEqual(output_lines[2], "請輸入\"結束\"日期 (yyyy-mm-dd):")
        self.assertEqual(output_lines[3], "Error: 時間區間至少一天")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=[0,1,2])
    @patch.object(ReportPage, 'hint_choose_report_IE')
    @patch.object(ReportPage, 'chooseReportType')
    def test_chooseReportIE(self, _chooseReportType, _hint_choose_report_IE, _input, _stdout):
        result = ReportPage.chooseReportIE('2023-01-01', '2023-04-30')
        self.assertEqual(result, False)
        result = ReportPage.chooseReportIE('2023-01-01', '2023-04-30')
        result = ReportPage.chooseReportIE('2023-01-01', '2023-04-30')
        self.assertEqual(_chooseReportType.call_count, 2)
        self.assertEqual(_hint_choose_report_IE.call_count, 3)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=[0, 1, 2])
    @patch.object(ReportPage, 'hint_choose_report_type')
    @patch.object(ReportPage, 'Report')
    def test_chooseReportType(self, _Report, _hint_choose_report_type, _input, _stdout):
        result = ReportPage.chooseReportType('2023-01-01', '2023-04-30', IEDirection.INCOME)
        self.assertEqual(result, False)
        result = ReportPage.chooseReportType('2023-01-01', '2023-04-30', IEDirection.INCOME)
        result = ReportPage.chooseReportType('2023-01-01', '2023-04-30', IEDirection.EXPENSE)
        self.assertEqual(_Report.call_count, 2)
        self.assertEqual(_hint_choose_report_type.call_count, 3)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_Report(self, _stdout):
        with self.mock_db_config:
            ReportPage.setUp_connection_and_table()
            result1 = ReportPage.Report('2023-01-01', '2023-03-30', IEDirection.INCOME, ReportByOption.category)
            result1 = ReportPage.Report('2023-01-01', '2023-03-30', IEDirection.EXPENSE, ReportByOption.category)
            result2 = ReportPage.Report('2023-05-01', '2023-05-19', IEDirection.EXPENSE, ReportByOption.account)
            result2 = ReportPage.Report('2023-05-01', '2023-05-23', IEDirection.INCOME, ReportByOption.account)
            ReportPage.tearDown_connection(es.NONE)
        self.assertEqual(result1, True)
        self.assertEqual(result2, True)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "此區間無報表可以顯示")
        self.assertEqual(output_lines[1], "\"飲料\" 總金額:101.0 百分比:17%")
        self.assertEqual(output_lines[2], "\"食物\" 總金額:157.0 百分比:27%")
        self.assertEqual(output_lines[3], "\"衣服\" 總金額:321.0 百分比:56%")
        self.assertEqual(output_lines[4], "支出總金額:579.0 百分比:100%")
        self.assertEqual(output_lines[5], "\"現金\" 總金額:50.0 百分比:2%")
        self.assertEqual(output_lines[6], "\"Line Pay\" 總金額:2600.0 百分比:98%")
        self.assertEqual(output_lines[7], "支出總金額:2650.0 百分比:100%")
        self.assertEqual(output_lines[8], "\"中華郵政\" 總金額:10000.0 百分比:100%")
        self.assertEqual(output_lines[9], "收入總金額:10000.0 百分比:100%")

    @patch.object(ReportPage, 'execute')
    @patch.object(ReportPage, 'choose', side_effect=[ReportOption.CHOOSE, ReportOption.BACK])
    @patch.object(ReportPage, 'show')
    def test_start(self, _show, _choose, _execute):
        ReportPage.start()
        self.assertEqual(_show.call_count, 2)
        self.assertEqual(_choose.call_count, 2)
        self.assertEqual(_execute.call_count, 1)
