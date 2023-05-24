import io
from unittest.mock import patch
from fixedIE import FixedIEPage, FixedIEOption, FixedIEType
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
        hints_argc1 = [(FixedIEPage.hint_create_name, FixedIEType.INCOME,  "請輸入新的固定收入名稱:\n"),
                       (FixedIEPage.hint_create_name, FixedIEType.EXPENSE, "請輸入新的固定支出名稱:\n")]
        hints_argc0 = [(FixedIEPage.hint_create_day, "請輸入每月收支日(1-31):\n"),
                       (FixedIEPage.hint_select_update_name, "請輸入要修改的固定收支的名稱:\n"),
                       (FixedIEPage.hint_update_option, "請選擇要修改的項目(1 類別, 2 帳戶, 3 金額, 4 地點, 5 時間, 6 備註, 7 返回):\n"),
                       (FixedIEPage.hint_update_day, "修改每月收支日為(1-31):\n"),
                       (FixedIEPage.hint_delete_name, "請輸入要刪除的固定收支的名稱:\n"),
                       (FixedIEPage.hintDayErorMsg, "請輸入 1 到 31 之間的數字:\n"),
                       (FixedIEPage.hintGetCategory, "請輸入紀錄類型:\n"),
                       (FixedIEPage.hintGetAccount, "請輸入帳戶:\n"),
                       (FixedIEPage.hintGetAmount, "請輸入金額:\n"),
                       (FixedIEPage.hintGetLocation, "請輸入地點:\n"),
                       (FixedIEPage.hintGetNote, "請輸入備註:\n")
                       ]
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
    """
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
    @patch('builtins.input', side_effect=[ 3, 1, "獎學金", 0 ,2 , 0, 5, "一萬", 10000, 80, 25 , '', 2, "房租", 2, 5, 8000, 5, 'sos'])
    @patch.object(FixedIEPage, 'hint_create_note')
    @patch.object(FixedIEPage, 'hint_create_day')
    @patch.object(FixedIEPage, 'hint_create_account')
    @patch.object(FixedIEPage, 'hint_create_category')
    @patch.object(FixedIEPage, 'hint_create_amount')
    @patch.object(FixedIEPage, 'hint_create_name')
    @patch.object(FixedIEPage, 'hint_create_type')
    def test_create(self, _hint_create_type, _hint_create_name, _hint_create_amount, _hint_create_category, _hint_create_account, _hint_create_day, _hint_create_note, _input, _stdout):
        with self.mock_db_config:
            FixedIEPage.setUp_connection_and_table()
            FixedIEPage.create()
            FixedIEPage.create()
            FixedIEPage.tearDown_connection(es.NONE)
        self.assertEqual(_hint_create_type.call_count, 2)
        self.assertEqual(_hint_create_name.call_count, 2)
        self.assertEqual(_hint_create_amount.call_count, 2)
        self.assertEqual(_hint_create_category.call_count, 2)
        self.assertEqual(_hint_create_account.call_count, 2)
        self.assertEqual(_input.call_count, 19)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "請輸入 1 到 2 之間的數字:")
        self.assertEqual(output_lines[1], "請輸入 1 到 3 之間的數字:")
        self.assertEqual(output_lines[2], "請輸入 1 到 5 之間的數字:")
        self.assertEqual(output_lines[3], "請輸入數字:")
        self.assertEqual(output_lines[4], "請輸入 1 到 31 之間的數字:")

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read(self, _stdout):
        with self.mock_db_config:
            FixedIEPage.setUp_connection_and_table()
            FixedIEPage.read()
            FixedIEPage.tearDown_connection(es.NONE)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "INCOME 名稱\"獎學金\" 類別OTHER 帳戶OTHER 金額10000.0 每月15號 備註:")
        self.assertEqual(output_lines[1], "EXPENSE 名稱\"房租\" 類別OTHER 帳戶OTHER 金額6000.0 每月20號 備註:sos")

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=["獎學金", 0, 3, "房租", 4, "unknown", "房租", 6])
    @patch.object(FixedIEPage, 'hint_update_option')
    @patch.object(FixedIEPage, 'hint_select_update_name')
    @patch.object(FixedIEPage, 'update_day')
    @patch.object(FixedIEPage, 'update_amount')
    @patch.object(FixedIEPage, 'read')
    def test_update(self, _read, _update_amount, _update_day, _hint_select_update_name, _hint_update_option, _input, _stdout):
        with self.mock_db_config:
            FixedIEPage.setUp_connection_and_table()
            FixedIEPage.update()
            FixedIEPage.read()

            FixedIEPage.update()
            FixedIEPage.read()

            FixedIEPage.update()
            FixedIEPage.read()

            result = FixedIEPage.update()

            FixedIEPage.tearDown_connection(es.NONE)
        self.assertEqual(result, True)
        self.assertEqual(_read.call_count, 3)
        self.assertEqual(_update_amount.call_count, 1)
        self.assertEqual(_update_day.call_count, 1)
        self.assertEqual(_hint_select_update_name.call_count, 4)
        self.assertEqual(_hint_update_option.call_count, 3)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "請輸入 1 到 6 之間的數字:")
        self.assertEqual(output_lines[1], "未找到名稱為 \"unknown\" 的固定收支")

    def test_update_catrgory(self):
        pass

    def test_update_account(self):
        pass


    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=[8000,"八千", 12000, -1000, 8000])
    @patch.object(FixedIEPage, 'hint_update_format_amount')
    @patch.object(FixedIEPage, 'hint_update_amount')
    def test_update_amount(self, _hint_update_amount, _hint_update_format_amount, _input, _stdout):
        with self.mock_db_config:
            FixedIEPage.setUp_connection_and_table()
            FixedIEPage.update_amount("獎學金")
            FixedIEPage.update_amount("獎學金")
            FixedIEPage.update_amount("房租")
            FixedIEPage.tearDown_connection(es.NONE)
        self.assertEqual(_hint_update_amount.call_count, 3)
        self.assertEqual(_hint_update_format_amount.call_count, 2)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "名稱為 \"獎學金\" 的固定收支金額已成功更新為 8000.00")
        self.assertEqual(output_lines[1], "名稱為 \"獎學金\" 的固定收支金額已成功更新為 12000.00")
        self.assertEqual(output_lines[2], "名稱為 \"房租\" 的固定收支金額已成功更新為 8000.00")
    """
    def test_update_day(self):
        pass

    def test_update_note(self):
        pass

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=["獎學金", "unknown", "房租"])
    @patch.object(FixedIEPage, 'hint_delete_name')
    @patch.object(FixedIEPage, 'read')
    def test_delete(self, _read, _hint_delete_name, _input, _stdout):
        with self.mock_db_config:
            FixedIEPage.setUp_connection_and_table()
            self.assertEqual(FixedIEPage.delete(), True)
            FixedIEPage.read()
            self.assertEqual(FixedIEPage.delete(), False)
            FixedIEPage.read()
            self.assertEqual(FixedIEPage.delete(), True)
            FixedIEPage.read()
            FixedIEPage.tearDown_connection(es.NONE)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "名稱為 \"獎學金\" 的固定收支已成功刪除")
        self.assertEqual(output_lines[1], "未找到名稱為 \"unknown\" 的固定收支")
        self.assertEqual(output_lines[2], "名稱為 \"房租\" 的固定收支已成功刪除")
        self.assertEqual(_read.call_count, 3)

    @patch.object(FixedIEPage, 'execute')
    @patch.object(FixedIEPage, 'choose', side_effect=[FixedIEOption.CREATE, FixedIEOption.READ, FixedIEOption.UPDATE, FixedIEOption.DELETE, FixedIEOption.BACK])
    @patch.object(FixedIEPage, 'show')
    def test_start(self, _show, _choose, _execute):
        FixedIEPage.start()
        self.assertEqual(_show.call_count, 5)
        self.assertEqual(_choose.call_count, 5)
        self.assertEqual(_execute.call_count, 4)