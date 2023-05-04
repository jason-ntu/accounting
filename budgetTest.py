import io
from unittest.mock import patch
from budget import BudgetPage, BudgetOption
from mock_db import MockDB

class TestUtils(MockDB):
        
    def setUp(self) -> None:
        self.budgetPage = BudgetPage()

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_show(self, _stdout):
        self.budgetPage.show()
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "%d: 查看總預算" % BudgetOption.READ)
        self.assertEqual(output_lines[1], "%d: 修改總預算" % BudgetOption.UPDATE)
        self.assertEqual(output_lines[2], "%d: 回到上一頁" % BudgetOption.BACK)
    
    @patch('builtins.input', side_effect=['0', '4', 'T', 'yes', 'false','3'])
    def test_choose(self, _input):
        self.assertEqual(self.budgetPage.choose(), 3)
        self.assertEqual(_input.call_count, 6)
    
    @patch.object(BudgetPage, 'update')
    @patch.object(BudgetPage, 'read')
    def test_execute(self, _read, _update):
        self.budgetPage.execute(BudgetOption.READ)
        self.assertEqual(_read.call_count, 1)
        self.budgetPage.execute(BudgetOption.UPDATE)
        self.assertEqual(_update.call_count, 1)
        with self.assertRaisesRegex(ValueError, self.budgetPage.errorMsg):
            self.budgetPage.execute(0)
    
    def test_read(self):
        with self.mock_db_config:
            self.assertEqual(self.budgetPage.read(), 10000)
    
    @patch('builtins.input', side_effect=['XYZ', 12345])
    @patch.object(BudgetPage, 'hint')
    def test_update(self, _hint, _input):
        with self.mock_db_config:
            self.assertEqual(self.budgetPage.update(), True)
            self.assertEqual(self.budgetPage.read(), 12345)
        self.assertEqual(_hint.call_count, 1)
        self.assertEqual(_input.call_count, 2)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_hint(self, _stdout):
        self.budgetPage.hint()
        self.assertEqual(_stdout.getvalue(), "請輸入新的總預算:\n")

    @patch.object(BudgetPage, 'execute')
    @patch.object(BudgetPage, 'choose', side_effect=[BudgetOption.READ, BudgetOption.UPDATE, BudgetOption.BACK])
    @patch.object(BudgetPage, 'show')
    def test_start(self, _show, _choose, _execute):
        self.budgetPage.start()
        self.assertEqual(_show.call_count, 3)
        self.assertEqual(_choose.call_count, 3)
        self.assertEqual(_execute.call_count, 2)
