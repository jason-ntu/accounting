from unittest import TestCase
from unittest.mock import patch
import io
from settings import SettingsPage, SettingsOption
from budget import BudgetPage
from fixedIE import FixedIE
from category import Category
from balance import Balance
from location import Location

class TestSettings(TestCase):

    def setUp(self) -> None:
        self.settingsPage = SettingsPage()

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_show(self, _stdout):
        self.settingsPage.show()
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "%d: 查看/修改總預算" % SettingsOption.BUDGET)
        self.assertEqual(output_lines[1], "%d: 新增每月固定收支" % SettingsOption.FIXEDIE)
        self.assertEqual(output_lines[2], "%d: 查看/新增/修改/刪除類別" % SettingsOption.CATEGORY)
        self.assertEqual(output_lines[3], "%d: 查看/新增/修改/刪除餘額" % SettingsOption.BALANCE)
        self.assertEqual(output_lines[4], "%d: 查看/新增/修改/刪除地點" % SettingsOption.LOCATION)
        self.assertEqual(output_lines[5], "%d: 回到上一頁" % SettingsOption.BACK)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['0', '7', 'T', 'yes', 'false','2'])
    def test_choose(self, _input,  _stdout):
        self.assertEqual(self.settingsPage.choose(), 2)
        self.assertEqual(_input.call_count, 6)
        self.assertEqual(_stdout.getvalue(), (self.settingsPage.errorMsg + "\n")*5)

    @patch.object(Location, 'start')
    @patch.object(Balance, 'start')
    @patch.object(Category, 'start')
    @patch.object(FixedIE, 'start')
    @patch.object(BudgetPage, 'start')
    def test_enter(self, _budget_start, _fixedIE_start, _category_start, _balance_start, _location_start):
        self.settingsPage.enter(SettingsOption.BUDGET)
        self.assertEqual(_budget_start.call_count, 1)
        self.settingsPage.enter(SettingsOption.FIXEDIE)
        self.assertEqual(_fixedIE_start.call_count, 1)
        self.settingsPage.enter(SettingsOption.CATEGORY)
        self.assertEqual(_category_start.call_count, 1)
        self.settingsPage.enter(SettingsOption.BALANCE)
        self.assertEqual(_balance_start.call_count, 1)
        self.settingsPage.enter(SettingsOption.LOCATION)
        self.assertEqual(_location_start.call_count, 1)
        with self.assertRaisesRegex(ValueError, self.settingsPage.errorMsg):
            self.settingsPage.enter(0)
        

    @patch.object(SettingsPage, 'enter')
    @patch.object(SettingsPage, 'choose', side_effect=[SettingsOption.BUDGET, SettingsOption.BACK])
    @patch.object(SettingsPage, 'show')
    def test_start(self, _show, _choose, _enter):
        self.settingsPage.start()
        self.assertEqual(_show.call_count, 2)
        self.assertEqual(_choose.call_count, 2)
        self.assertEqual(_enter.call_count, 1)
