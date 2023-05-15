import io
from unittest.mock import patch
from income import IncomePage, IncomeOption
from mock_db import MockDB
from accessor import ExecutionStatus as es
import const

class TestIncomePage(MockDB):

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_show(self, _stdout):
        IncomePage.show()
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "[收入設定]")
        self.assertEqual(output_lines[1], "%d: 新增收入方式" % IncomeOption.CREATE)
        self.assertEqual(output_lines[2], "%d: 查看收入方式" % IncomeOption.READ)
        self.assertEqual(output_lines[3], "%d: 修改收入方式" % IncomeOption.UPDATE)
        self.assertEqual(output_lines[4], "%d: 刪除收入方式" % IncomeOption.DELETE)
        self.assertEqual(output_lines[5], "%d: 回到上一頁" % IncomeOption.BACK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_hints(self, _stdout):
        hints = [(IncomePage.hint_create_name, "請輸入新收入方式的...\n名稱:\n"),
                 (IncomePage.hint_update_name, "請選擇要修改的收入方式(輸入名稱):\n"),
                 (IncomePage.hint_update_new_name, "請輸入新的名稱:\n"),
                 (IncomePage.hint_delete, "請選擇要刪除的收入方式(輸入名稱):\n")]
        for hint in hints:
            hint[0]()
            self.assertMultiLineEqual(_stdout.getvalue(), hint[1])
            _stdout.truncate(0)
            _stdout.seek(0)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['0', '6', 'T', '1', '2', '3', '4', '5'])
    def test_choose(self, _input,  _stdout):
        self.assertEqual(IncomePage.choose(), IncomeOption.CREATE)
        self.assertEqual(_input.call_count, 4)
        self.assertEqual(_stdout.getvalue(), "請輸入 1 到 5 之間的數字:\n"*3)
        self.assertEqual(IncomePage.choose(), IncomeOption.READ)
        self.assertEqual(_input.call_count, 5)
        self.assertEqual(IncomePage.choose(), IncomeOption.UPDATE)
        self.assertEqual(_input.call_count, 6)
        self.assertEqual(IncomePage.choose(), IncomeOption.DELETE)
        self.assertEqual(_input.call_count, 7)
        self.assertEqual(IncomePage.choose(), IncomeOption.BACK)
        self.assertEqual(_input.call_count, 8)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(IncomePage, 'delete', return_value=True)
    @patch.object(IncomePage, 'update', return_value=False)
    @patch.object(IncomePage, 'read')
    @patch.object(IncomePage, 'create', return_value=True)
    def test_execute(self, _create, _read, _update, _delete, _stdout):
        with self.mock_db_config:
            IncomePage.execute(IncomeOption.CREATE)
            self.assertEqual(_create.call_count, 1)
            IncomePage.execute(IncomeOption.READ)
            self.assertEqual(_read.call_count, 1)
            IncomePage.execute(IncomeOption.UPDATE)
            self.assertEqual(_update.call_count, 1)
            IncomePage.execute(IncomeOption.DELETE)
            self.assertEqual(_delete.call_count, 1)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "%s操作成功%s" %
                         (const.ANSI_GREEN, const.ANSI_RESET))
        self.assertEqual(output_lines[1], "%s操作失敗%s" %
                         (const.ANSI_RED, const.ANSI_RESET))
        self.assertEqual(output_lines[2], "%s操作成功%s" %
                         (const.ANSI_GREEN, const.ANSI_RESET))

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=["獎金", "", "紅包"])
    @patch.object(IncomePage, 'hint_create_name')
    def test_create(self, _hint_create_name, _input, _stdout):
        with self.mock_db_config:
            IncomePage.setUp_connection_and_table()
            IncomePage.create()
            IncomePage.create()
            IncomePage.create()
            IncomePage.read()
            IncomePage.tearDown_connection(es.NONE)
        self.assertEqual(_hint_create_name.call_count, 3)
        self.assertEqual(_input.call_count, 3)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "%s新名稱不得與其他收入的名稱重複%s" % (const.ANSI_YELLOW, const.ANSI_RESET))
        self.assertEqual(output_lines[1], "%s名稱不得為空%s" % (const.ANSI_YELLOW, const.ANSI_RESET))
        self.assertEqual(output_lines[2], "\"獎金\"")
        self.assertEqual(output_lines[3], "\"退款\"")
        self.assertEqual(output_lines[4], "\"回饋\"")
        self.assertEqual(output_lines[5], "\"其他\"")
        self.assertEqual(output_lines[6], "\"紅包\"")

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read(self, _stdout):
        with self.mock_db_config:
            IncomePage.setUp_connection_and_table()
            IncomePage.read()
            IncomePage.tearDown_connection(es.NONE)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "\"獎金\"")
        self.assertEqual(output_lines[1], "\"退款\"")
        self.assertEqual(output_lines[2], "\"回饋\"")
        self.assertEqual(output_lines[3], "\"其他\"")

    def test_update(self):
        pass

    def test_delete(self):
        pass

    @patch.object(IncomePage, 'execute')
    @patch.object(IncomePage, 'choose', side_effect=[IncomeOption.CREATE, IncomeOption.READ, IncomeOption.UPDATE, IncomeOption.DELETE, IncomeOption.BACK])
    @patch.object(IncomePage, 'show')
    def test_start(self, _show, _choose, _execute):
        IncomePage.start()
        self.assertEqual(_show.call_count, 5)
        self.assertEqual(_choose.call_count, 5)
        self.assertEqual(_execute.call_count, 4)
