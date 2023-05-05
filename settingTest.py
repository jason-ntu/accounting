from unittest import TestCase
from unittest.mock import patch
import io
from setting import SettingPage, SettingOption
from budget import BudgetPage
from fixedIE import FixedIE
from category import Category
from payment import PaymentPage
from location import Location



class TestSetting(TestCase):

    def setUp(self) -> None:
        self.settingPage = SettingPage()

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_show(self, _stdout):
        self.settingPage.show()
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "%d: 查看/修改總預算" % SettingOption.BUDGET)
        self.assertEqual(output_lines[1], "%d: 新增每月固定收支" % SettingOption.FIXEDIE)
        self.assertEqual(output_lines[2], "%d: 查看/新增/修改/刪除類別" % SettingOption.CATEGORY)
        self.assertEqual(output_lines[3], "%d: 查看/新增/修改/刪除餘額" % SettingOption.BALANCE)
        self.assertEqual(output_lines[4], "%d: 查看/新增/修改/刪除地點" % SettingOption.LOCATION)
        self.assertEqual(output_lines[5], "%d: 回到上一頁" % SettingOption.BACK)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['0', '7', 'T', '1', '2', '3', '4', '5', '6'])
    def test_choose(self, _input,  _stdout):
        self.assertEqual(self.settingPage.choose(), 1)
        self.assertEqual(_input.call_count, 4)
        self.assertEqual(_stdout.getvalue(), ("請輸入 1 到 6 之間的整數:\n")*3)
        self.assertEqual(self.settingPage.choose(), 2)
        self.assertEqual(_input.call_count, 5)
        self.assertEqual(self.settingPage.choose(), 3)
        self.assertEqual(_input.call_count, 6)
        self.assertEqual(self.settingPage.choose(), 4)
        self.assertEqual(_input.call_count, 7)
        self.assertEqual(self.settingPage.choose(), 5)
        self.assertEqual(_input.call_count, 8)
        self.assertEqual(self.settingPage.choose(), 6)
        self.assertEqual(_input.call_count, 9)

    @patch.object(Location, 'start')
    @patch.object(PaymentPage, 'start')
    @patch.object(Category, 'start')
    @patch.object(FixedIE, 'start')
    @patch.object(BudgetPage, 'start')
    def test_enter(self, _budget_start, _fixedIE_start, _category_start, _balance_start, _location_start):
        self.settingPage.enter(SettingOption.BUDGET)
        self.assertEqual(_budget_start.call_count, 1)
        self.settingPage.enter(SettingOption.FIXEDIE)
        self.assertEqual(_fixedIE_start.call_count, 1)
        self.settingPage.enter(SettingOption.CATEGORY)
        self.assertEqual(_category_start.call_count, 1)
        self.settingPage.enter(SettingOption.BALANCE)
        self.assertEqual(_balance_start.call_count, 1)
        self.settingPage.enter(SettingOption.LOCATION)
        self.assertEqual(_location_start.call_count, 1)

    @patch.object(SettingPage, 'enter')
    @patch.object(SettingPage, 'choose', side_effect=[SettingOption.BUDGET, SettingOption.BACK])
    @patch.object(SettingPage, 'show')
    def test_start(self, _show, _choose, _enter):
        self.settingPage.start()
        self.assertEqual(_show.call_count, 2)
        self.assertEqual(_choose.call_count, 2)
        self.assertEqual(_enter.call_count, 1)
