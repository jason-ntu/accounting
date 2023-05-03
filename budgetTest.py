import budget
import unittest
from unittest.mock import patch
from structure import Action
import io

class TestSetting(unittest.TestCase):
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_showBudgetPage(self, _stdout):
        budget.showBudgetPage()
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "%d: 查看總預算" % Action.READ)
        self.assertEqual(output_lines[1], "%d: 修改總預算" % Action.UPDATE)
    
    @patch.object(budget, 'readBudget')
    @patch('builtins.input', side_effect=['3', 'yes','1'])
    @patch.object(budget, 'showBudgetPage')
    def test_enterBudgetPage_input_invalids_and_read(self, _showBudgetPage, _input, _readBudget):        
        budget.enterBudgetPage()
        self.assertEqual(_showBudgetPage.call_count, 1)
        self.assertEqual(_input.call_count, 3)        
        self.assertEqual(_readBudget.call_count, 1)
    
    @patch.object(budget, 'updateBudget')
    @patch('builtins.input', side_effect=['2'])
    @patch.object(budget, 'showSettingsPage')
    def test_enterSettingsPage_input_fixedIE(self, _showSettingsPage, _input, _updateBudget):
        budget.enterBudgetPage()
        self.assertEqual(_showSettingsPage.call_count, 1)
        self.assertEqual(_input.call_count, 1)        
        self.assertEqual(_updateBudget.call_count, 1)
    