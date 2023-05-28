import io
from unittest.mock import patch
from fixedIE import FixedIEPage, FixedIEOption
from IEDirection import IEDirection
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
        hints_argc1 = [(FixedIEPage.hint_create_name, IEDirection.INCOME,  "請輸入新的固定收入名稱:\n"),
                       (FixedIEPage.hint_create_name, IEDirection.EXPENSE, "請輸入新的固定支出名稱:\n")]
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
    
    @patch.object(FixedIEPage, 'askNote', side_effect=["random", "筆記"])
    @patch.object(FixedIEPage, 'askDay', side_effect=[1, 31])
    @patch.object(FixedIEPage, 'hint_create_day')
    @patch.object(FixedIEPage, 'askLocation', side_effect=["收入地點", "支出地點"])
    @patch.object(FixedIEPage, 'askAmount', side_effect=[123.4, 10])
    @patch.object(FixedIEPage, 'askAccount', side_effect=[{'name': "帳號A"}, {'name': "帳號B"}])
    @patch.object(FixedIEPage, 'askCategory', side_effect=["收入類別", "支出類別"])
    @patch.object(FixedIEPage, 'hint_create_name')
    @patch.object(FixedIEPage, 'askIE', side_effect=[IEDirection.INCOME, IEDirection.EXPENSE])
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=["固定收入", "固定支出"])
    def test_create_and_read(self, _input, _stdout, _askIE, _hint_create_name, _askCategory, _askAccount, _askAmount, _askLocation, _hint_create_day, _askDay, _askNote):
        outputs = [
            "INCOME 名稱\"固定收入\" 類別收入類別 帳戶帳號A 金額123.4 地點收入地點 每月1號 備註:random",
            "EXPENSE 名稱\"固定支出\" 類別支出類別 帳戶帳號B 金額10.0 地點支出地點 每月31號 備註:筆記"
        ]
        for i in range(2):
            with self.subTest(i=i):
                with self.mock_db_config:
                    FixedIEPage.setUp_connection_and_table()
                    FixedIEPage.create()
                    FixedIEPage.read()
                    FixedIEPage.tearDown_connection(es.NONE)
                self.assertEqual(_askIE.call_count, i+1)
                self.assertEqual(_hint_create_name.call_count, i+1)
                self.assertEqual(_askCategory.call_count, i+1)
                self.assertEqual(_askAccount.call_count, i+1)
                self.assertEqual(_askAmount.call_count, i+1)
                self.assertEqual(_askLocation.call_count, i+1)
                self.assertEqual(_hint_create_day.call_count, i+1)
                self.assertEqual(_askDay.call_count, i+1)
                self.assertEqual(_askNote.call_count, i+1)
                self.assertEqual(_stdout.getvalue().strip().split('\n')[-1], outputs[i])
                _stdout.truncate(0)
                _stdout.seek(0)

    @patch.object(FixedIEPage, 'hintDayErorMsg')
    @patch('builtins.input', side_effect=[1, 0, 32, 31])
    def test_askDay(self, _input, _hintDayErorMsg):
        result = FixedIEPage.askDay()
        self.assertEqual(_input.call_count, 1)
        self.assertEqual(_hintDayErorMsg.call_count, 0)
        self.assertEqual(result, 1)

        result = FixedIEPage.askDay()
        self.assertEqual(_input.call_count, 4)
        self.assertEqual(_hintDayErorMsg.call_count, 2)
        self.assertEqual(result, 31)
    
    @patch.object(FixedIEPage, 'update_note', return_value=True) # spies[5]
    @patch.object(FixedIEPage, 'update_day', return_value=True) # spies[4]
    @patch.object(FixedIEPage, 'update_location', return_value=True) # spies[3]
    @patch.object(FixedIEPage, 'update_amount', return_value=True) # spies[2]
    @patch.object(FixedIEPage, 'update_account', return_value=True) # spies[1]
    @patch.object(FixedIEPage, 'update_category', return_value=True) # spies[0]
    @patch.object(FixedIEPage, 'hint_update_option')
    @patch.object(FixedIEPage, 'hint_select_update_name')
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=[
        "unknow",
        "獎學金", 0, 1,
        "獎學金", "X", 2,
        "獎學金", "T", 3,
        "獎學金", "Yes", 4,
        "獎學金", "", 5,
        "獎學金", -1, 6,
        "獎學金", 8, 7
        ])
    def test_update(self, _input, _stdout, _hint_select_update_name, _hint_update_option, *spies):
        for i in range(8):
            with self.subTest(i for i in range(8)):
                with self.mock_db_config:
                        FixedIEPage.setUp_connection_and_table()
                        result = FixedIEPage.update()
                        FixedIEPage.tearDown_connection(es.NONE)
                self.assertEqual(_input.call_count, 3*i+1)
                self.assertEqual(_hint_select_update_name.call_count, i+1)
                self.assertEqual(_hint_update_option.call_count, i)
                if i == 0:
                    self.assertEqual(result, False)
                    self.assertEqual(_stdout.getvalue(), "未找到名稱為 \"unknow\" 的固定收支\n")
                else:
                    if i in range(1, 7):
                        self.assertEqual(spies[i-1].call_count, 1)
                    self.assertEqual(result, True)
                    self.assertEqual(_stdout.getvalue(), "請輸入 1 到 7 之間的數字:\n")
                _stdout.truncate(0)
                _stdout.seek(0)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(FixedIEPage, 'askCategory', return_value="新類別")
    def test_update_catrgory(self, _askCategory, _stdout):
        with self.mock_db_config:
            FixedIEPage.setUp_connection_and_table()
            result = FixedIEPage.update_category("獎學金")
            FixedIEPage.tearDown_connection(es.NONE)
        self.assertEqual(_askCategory.call_count, 1)
        self.assertEqual(result, True)
        self.assertEqual(_stdout.getvalue(), "名稱為 \"獎學金\" 的固定收支類別已成功更新為 新類別\n")

        with self.mock_db_config:
            FixedIEPage.setUp_connection_and_table()
            result = FixedIEPage.update_category("unknow")
            FixedIEPage.tearDown_connection(es.NONE)
        self.assertEqual(_askCategory.call_count, 2)
        self.assertEqual(result, False)
        
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(FixedIEPage, 'askAccount', return_value={'name': "新帳戶"})
    def test_update_account(self, _askAccount, _stdout):
        with self.mock_db_config:
            FixedIEPage.setUp_connection_and_table()
            result = FixedIEPage.update_account("獎學金")
            FixedIEPage.tearDown_connection(es.NONE)
        self.assertEqual(_askAccount.call_count, 1)
        self.assertEqual(result, True)
        self.assertEqual(_stdout.getvalue(), "名稱為 \"獎學金\" 的固定收支帳戶已成功更新為 新帳戶\n")

        with self.mock_db_config:
            FixedIEPage.setUp_connection_and_table()
            result = FixedIEPage.update_account("unknow")
            FixedIEPage.tearDown_connection(es.NONE)
        self.assertEqual(_askAccount.call_count, 2)
        self.assertEqual(result, False)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(FixedIEPage, 'askAmount', return_value=1234.56)
    def test_update_amount(self, _askAmount, _stdout):
        with self.mock_db_config:
            FixedIEPage.setUp_connection_and_table()
            result = FixedIEPage.update_amount("獎學金")
            FixedIEPage.tearDown_connection(es.NONE)
        self.assertEqual(_askAmount.call_count, 1)
        self.assertEqual(result, True)
        self.assertEqual(_stdout.getvalue(), "名稱為 \"獎學金\" 的固定收支金額已成功更新為 1234.56\n")

        with self.mock_db_config:
            FixedIEPage.setUp_connection_and_table()
            result = FixedIEPage.update_amount("unknow")
            FixedIEPage.tearDown_connection(es.NONE)
        self.assertEqual(_askAmount.call_count, 2)
        self.assertEqual(result, False)

    
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(FixedIEPage, 'askLocation', return_value="新地點")
    def test_update_location(self, _askLocation, _stdout):
        with self.mock_db_config:
            FixedIEPage.setUp_connection_and_table()
            result = FixedIEPage.update_location("獎學金")
            FixedIEPage.tearDown_connection(es.NONE)
        self.assertEqual(_askLocation.call_count, 1)
        self.assertEqual(result, True)
        self.assertEqual(_stdout.getvalue(), "名稱為 \"獎學金\" 的固定收支地點已成功更新為 新地點\n")

        with self.mock_db_config:
            FixedIEPage.setUp_connection_and_table()
            result = FixedIEPage.update_location("unknow")
            FixedIEPage.tearDown_connection(es.NONE)
        self.assertEqual(_askLocation.call_count, 2)
        self.assertEqual(result, False)


    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(FixedIEPage, 'askDay', return_value=15)
    @patch.object(FixedIEPage, 'hint_update_day')
    def test_update_day(self, _hint_update_day, _askDay, _stdout):
        with self.mock_db_config:
            FixedIEPage.setUp_connection_and_table()
            result = FixedIEPage.update_day("獎學金")
            FixedIEPage.tearDown_connection(es.NONE)
        self.assertEqual(_hint_update_day.call_count, 1)
        self.assertEqual(_askDay.call_count, 1)
        self.assertEqual(result, True)
        self.assertEqual(_stdout.getvalue(), "名稱為 \"獎學金\" 的固定收支時間已成功更新為每月 15 號\n")

        with self.mock_db_config:
            FixedIEPage.setUp_connection_and_table()
            result = FixedIEPage.update_day("unknow")
            FixedIEPage.tearDown_connection(es.NONE)
        self.assertEqual(_hint_update_day.call_count, 2)
        self.assertEqual(_askDay.call_count, 2)
        self.assertEqual(result, False)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(FixedIEPage, 'askNote', return_value="新備註")
    def test_update_note(self, _askNote, _stdout):
        with self.mock_db_config:
            FixedIEPage.setUp_connection_and_table()
            result = FixedIEPage.update_note("獎學金")
            FixedIEPage.tearDown_connection(es.NONE)
        self.assertEqual(_askNote.call_count, 1)
        self.assertEqual(result, True)
        self.assertEqual(_stdout.getvalue(), "名稱為 \"獎學金\" 的固定收支備註已成功更新為 新備註\n")

        with self.mock_db_config:
            FixedIEPage.setUp_connection_and_table()
            result = FixedIEPage.update_note("unknow")
            FixedIEPage.tearDown_connection(es.NONE)
        self.assertEqual(_askNote.call_count, 2)
        self.assertEqual(result, False)

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