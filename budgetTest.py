import io
from unittest.mock import patch
from budget import BudgetPage, BudgetOption
from mock_db import MockDB
from accessor import ExecutionStatus as es
import const


class TestBudgetPage(MockDB):
    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_show(self, _stdout):
    #     BudgetPage.show()
    #     output_lines = _stdout.getvalue().strip().split("\n")
    #     self.assertEqual(output_lines[0], "%d: 查看總預算" % BudgetOption.READ)
    #     self.assertEqual(output_lines[1], "%d: 修改總預算" % BudgetOption.UPDATE)
    #     self.assertEqual(output_lines[2], "%d: 回到上一頁" % BudgetOption.BACK)

    # @patch("sys.stdout", new_callable=io.StringIO)
    # @patch("builtins.input", side_effect=["0", "4", "F", "1", "2", "3"])
    # def test_choose(self, _input, _stdout):
    #     self.assertEqual(BudgetPage.choose(), 1)
    #     self.assertEqual(_input.call_count, 4)
    #     self.assertEqual(_stdout.getvalue(), "請輸入 1 到 3 之間的數字:\n" * 3)
    #     self.assertEqual(BudgetPage.choose(), 2)
    #     self.assertEqual(_input.call_count, 5)
    #     self.assertEqual(BudgetPage.choose(), 3)
    #     self.assertEqual(_input.call_count, 6)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(BudgetPage, "update", side_effect=[True, False])
    @patch.object(BudgetPage, "read")
    def test_execute(self, _read, _update, _stdout):
        with self.mock_db_config:
            BudgetPage.execute(BudgetOption.READ)
            self.assertEqual(_read.call_count, 1)
            BudgetPage.execute(BudgetOption.UPDATE)
            BudgetPage.execute(BudgetOption.UPDATE)
            self.assertEqual(_update.call_count, 2)
        output_lines = _stdout.getvalue().strip().split("\n")
        self.assertEqual(output_lines[0], "%s操作成功%s" %
                         (const.ANSI_GREEN, const.ANSI_RESET))
        self.assertEqual(output_lines[1], "%s操作失敗%s" %
                         (const.ANSI_RED, const.ANSI_RESET))

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read(self, _stdout):
        with self.mock_db_config:
            BudgetPage.setUp_connection_and_table()
            BudgetPage.read()
            BudgetPage.tearDown_connection(es.NONE)
        self.assertEqual(_stdout.getvalue(), "10000.0\n")

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["XYZ", 12345, 12345.6])
    @patch.object(BudgetPage, "hint_update")
    def test_update(self, _hint_update, _input, _stdout):
        with self.mock_db_config:
            BudgetPage.setUp_connection_and_table()
            self.assertEqual(BudgetPage.update(), True)
            BudgetPage.read()
            self.assertEqual(BudgetPage.update(), True)
            BudgetPage.read()
            BudgetPage.tearDown_connection(es.NONE)
        self.assertEqual(_hint_update.call_count, 2)
        self.assertEqual(_input.call_count, 3)
        output_lines = _stdout.getvalue().strip().split("\n")
        self.assertEqual(output_lines[0], "請輸入數字:")
        self.assertEqual(output_lines[1], "12345.0")
        self.assertEqual(output_lines[2], "12345.6")

    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_hint_update(self, _stdout):
    #     BudgetPage.hint_update()
    #     self.assertEqual(_stdout.getvalue(), "請輸入新的總預算:\n")

    # @patch.object(BudgetPage, "execute")
    # @patch.object(
    #     BudgetPage,
    #     "choose",
    #     side_effect=[BudgetOption.READ, BudgetOption.UPDATE, BudgetOption.BACK],
    # )
    # @patch.object(BudgetPage, "show")
    # def test_start(self, _show, _choose, _execute):
    #     BudgetPage.start()
    #     self.assertEqual(_show.call_count, 3)
    #     self.assertEqual(_choose.call_count, 3)
    #     self.assertEqual(_execute.call_count, 2)
