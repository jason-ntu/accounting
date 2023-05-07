import io
from unittest.mock import patch, MagicMock
from income import IncomePage, IncomeOption, IncomeCategory
from mock_db import MockDB
from sqlalchemy import text

class TestIncomePage(MockDB):

    def setUp(self) -> None:
        self.incomePage = IncomePage()

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_show(self, _stdout):
        self.incomePage.show()
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "%d: 新增收入方式" % IncomeOption.CREATE)
        self.assertEqual(output_lines[1], "%d: 查看收入方式" % IncomeOption.READ)
        self.assertEqual(output_lines[2], "%d: 修改收入方式" % IncomeOption.UPDATE)
        self.assertEqual(output_lines[3], "%d: 刪除收入方式" % IncomeOption.DELETE)
        self.assertEqual(output_lines[4], "%d: 回到上一頁" % IncomeOption.BACK)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['0', '6', 'T', '1', '2', '3', '4', '5'])
    def test_choose(self, _input,  _stdout):
        self.assertEqual(self.incomePage.choose(), 1)
        self.assertEqual(_input.call_count, 4)
        self.assertEqual(_stdout.getvalue(), "請輸入 1 到 5 之間的數字:\n"*3)
        self.assertEqual(self.incomePage.choose(), 2)
        self.assertEqual(_input.call_count, 5)
        self.assertEqual(self.incomePage.choose(), 3)
        self.assertEqual(_input.call_count, 6)
        self.assertEqual(self.incomePage.choose(), 4)
        self.assertEqual(_input.call_count, 7)
        self.assertEqual(self.incomePage.choose(), 5)
        self.assertEqual(_input.call_count, 8)

    @patch.object(IncomePage, 'delete')
    @patch.object(IncomePage, 'update')
    @patch.object(IncomePage, 'read')
    @patch.object(IncomePage, 'create')
    def test_execute(self, _create, _read, _update, _delete):
        self.incomePage.execute(IncomeOption.CREATE)
        self.assertEqual(_create.call_count, 1)
        self.incomePage.execute(IncomeOption.READ)
        self.assertEqual(_read.call_count, 1)
        self.incomePage.execute(IncomeOption.UPDATE)
        self.assertEqual(_update.call_count, 1)
        self.incomePage.execute(IncomeOption.DELETE)
        self.assertEqual(_delete.call_count, 1)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_hint_create_name(self, _stdout):
        self.incomePage.hint_create_name()
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "請輸入新收入方式的...")
        self.assertEqual(output_lines[1], "名稱:")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_hint_create_amount(self, _stdout):
        self.incomePage.hint_create_amount()
        self.assertEqual(_stdout.getvalue(), "金額:\n")

    #def read(cls):
    #    pass

    #def format_print(results):
    #    pass

    #def update(cls):
    #    pass

    #def hint_update_original_name():
    #    pass

    #def hint_update_new_name():
    #    pass

    #def delete(cls):
    #    pass

    #def hint_delete_name():
    #    pass

    #def test_start(cls):
    #    pass


