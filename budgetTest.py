from unittest import TestCase
import io
from unittest.mock import patch
from budget import BudgetPage, BudgetOption
import utils


class TestBudget(TestCase):
        
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
            self.assertEqual(utils.db_read("""SELECT INTO `test_table` (`id`, `text`, `int`) VALUES
                            ('3', 'test_text_3', 3)"""), True)
            self.assertEqual(utils.db_write("""INSERT INTO `test_table` (`id`, `text`, `int`) VALUES
                            ('1', 'test_text_3', 3)"""), False)
            self.assertEqual(utils.db_write("""DELETE FROM `test_table` WHERE id='1' """), True)
            self.assertEqual(utils.db_write("""DELETE FROM `test_table` WHERE id='4' """), True)

        pass
    
    def test_update(self):
        pass

    @patch.object(BudgetPage, 'execute')
    @patch.object(BudgetPage, 'choose', side_effect=[BudgetOption.READ, BudgetOption.UPDATE, BudgetOption.BACK])
    @patch.object(BudgetPage, 'show')
    def test_start(self, _show, _choose, _execute):
        self.budgetPage.start()
        self.assertEqual(_show.call_count, 3)
        self.assertEqual(_choose.call_count, 3)
        self.assertEqual(_execute.call_count, 2)
