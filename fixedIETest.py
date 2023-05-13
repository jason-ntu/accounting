import io
from unittest.mock import patch
from fixedIE import FixedIEPage, FixedIEOption, FixedIECategory
from mock_db import MockDB
from accessor import ExecutionStatus as es
import const

class TestFixedIEPage(MockDB):

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_show(self, _stdout):
        FixedIEPage.show()
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "%d: 新增固定收支" % FixedIEOption.CREATE)
        self.assertEqual(output_lines[1], "%d: 查看固定收支" % FixedIEOption.READ)
        self.assertEqual(output_lines[2], "%d: 修改固定收支" % FixedIEOption.UPDATE)
        self.assertEqual(output_lines[3], "%d: 刪除固定收支" % FixedIEOption.DELETE)
        self.assertEqual(output_lines[4], "%d: 回到上一頁" % FixedIEOption.BACK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_hints(self, _stdout):
        hints_argc1 = [(FixedIEPage.hint_create_name, FixedIECategory.INCOME,  "請輸入新的固定收入...\n名稱:\n"),
                       (FixedIEPage.hint_create_name, FixedIECategory.EXPENSE, "請輸入新的固定支出...\n名稱:\n")]
        hints_argc0 = [(FixedIEPage.hint_create_amount, "金額:\n"),
                       (FixedIEPage.hint_create_category, "類型(1 固定收入, 2 固定支出):\n"),
                       (FixedIEPage.hint_select_update_name, "請輸入要修改的固定收支的名稱:\n"),
                       (FixedIEPage.hint_update_option, "請選擇要修改的項目(1 金額, 2 類別, 3 返回):\n"),
                       (FixedIEPage.hint_update_amount, "修改金額為:\n"),
                       (FixedIEPage.hint_update_category, "修改類型為(1 固定收入, 2 固定支出):\n"),
                       (FixedIEPage.hint_delete_name, "請輸入要刪除的固定收支的名稱:\n")]
        for hint in hints_argc1:
            hint[0](hint[1])
            self.assertMultiLineEqual(_stdout.getvalue(), hint[2])
            _stdout.truncate(0)
            _stdout.seek(0)

        for hint in hints_argc0:
            hint[0]()
            self.assertMultiLineEqual(_stdout.getvalue(), hint[1])
            _stdout.truncate(0)
            _stdout.seek(0)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['0', '6', 'T', '1', '2', '3', '4', '5'])
    def test_choose(self, _input,  _stdout):
        self.assertEqual(FixedIEPage.choose(), 1)
        self.assertEqual(_input.call_count, 4)
        self.assertEqual(_stdout.getvalue(), "請輸入 1 到 5 之間的數字:\n"*3)
        self.assertEqual(FixedIEPage.choose(), 2)
        self.assertEqual(_input.call_count, 5)
        self.assertEqual(FixedIEPage.choose(), 3)
        self.assertEqual(_input.call_count, 6)
        self.assertEqual(FixedIEPage.choose(), 4)
        self.assertEqual(_input.call_count, 7)
        self.assertEqual(FixedIEPage.choose(), 5)
        self.assertEqual(_input.call_count, 8)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(FixedIEPage, 'delete', return_value=True)
    @patch.object(FixedIEPage, 'update', return_value=False)
    @patch.object(FixedIEPage, 'read')
    @patch.object(FixedIEPage, 'create', return_value=True)
    def test_execute(self, _create, _read, _update, _delete, _stdout):
        with self.mock_db_config:
            FixedIEPage.execute(FixedIEOption.CREATE)
            self.assertEqual(_create.call_count, 1)
            FixedIEPage.execute(FixedIEOption.READ)
            self.assertEqual(_read.call_count, 1)
            FixedIEPage.execute(FixedIEOption.UPDATE)
            self.assertEqual(_update.call_count, 1)
            FixedIEPage.execute(FixedIEOption.DELETE)
            self.assertEqual(_delete.call_count, 1)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "%s操作成功%s" %
                         (const.ANSI_GREEN, const.ANSI_RESET))
        self.assertEqual(output_lines[1], "%s操作失敗%s" %
                         (const.ANSI_RED, const.ANSI_RESET))
        self.assertEqual(output_lines[2], "%s操作成功%s" %
                         (const.ANSI_GREEN, const.ANSI_RESET))

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=[ 3, 2, "獎學金", "一萬",10000,])
    @patch.object(FixedIEPage, 'hint_create_category')
    @patch.object(FixedIEPage, 'hint_create_amount')
    @patch.object(FixedIEPage, 'hint_create_name')
    def test_create(self, _hint_create_name, _hint_create_amount, _hint_create_category, _input, _stdout):
        with self.mock_db_config:
            FixedIEPage.setUp_connection_and_table()
            FixedIEPage.create()
            FixedIEPage.tearDown_connection(es.NONE)
        self.assertEqual(_hint_create_category.call_count, 1)
        self.assertEqual(_hint_create_name.call_count, 1)
        self.assertEqual(_hint_create_amount.call_count, 1)
        self.assertEqual(_input.call_count, 5)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "請輸入 1 到 2 之間的數字:")
        self.assertEqual(output_lines[1], "請輸入數字:")

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read(self, _stdout):
        with self.mock_db_config:
            FixedIEPage.setUp_connection_and_table()
            FixedIEPage.read()
            FixedIEPage.tearDown_connection(es.NONE)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "固定收支: 名稱\"獎學金\" 金額10000.0 類別INCOME")
        self.assertEqual(output_lines[1], "固定收支: 名稱\"房租\" 金額6000.0 類別EXPENSE")

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=["獎學金", 1, 8000])
    @patch.object(FixedIEPage, 'hint_update_category')
    @patch.object(FixedIEPage, 'hint_update_amount')
    @patch.object(FixedIEPage, 'hint_update_option')
    @patch.object(FixedIEPage, 'hint_select_update_name')
    @patch.object(FixedIEPage, 'update_category')
    @patch.object(FixedIEPage, 'update_amount')
    @patch.object(FixedIEPage, 'read')
    def test_update(self, _read, _update_amount, _update_category, _hint_select_update_name, _hint_update_option, _hint_update_amount, hint_update_category, _input, _stdout):
        pass

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=["獎學金", "unknown", "房租"])
    @patch.object(FixedIEPage, 'hint_delete_name')
    def test_delete(self, _hint_delete_name, _input, _stdout):
        #with self.mock_db_config:
        #    FixedIEPage.setUp_connection_and_table()
        #    self.assertEqual(FixedIEPage.delete(), True)
        #    self.assertEqual(FixedIEPage.delete(), False)
        #    self.assertEqual(FixedIEPage.delete(), True)
        #    FixedIEPage.tearDown_connection(es.NONE)
        pass


    @patch.object(FixedIEPage, 'execute')
    @patch.object(FixedIEPage, 'choose', side_effect=[FixedIEOption.CREATE, FixedIEOption.READ, FixedIEOption.UPDATE, FixedIEOption.DELETE, FixedIEOption.BACK])
    @patch.object(FixedIEPage, 'show')
    def test_start(self, _show, _choose, _execute):
        FixedIEPage.start()
        self.assertEqual(_show.call_count, 5)
        self.assertEqual(_choose.call_count, 5)
        self.assertEqual(_execute.call_count, 4)