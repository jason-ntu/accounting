from enum import IntEnum, auto
from budget import BudgetPage
from fixedIE import FixedIE
from category import Category
from payment import PaymentPage
from location import Location

class SettingOption(IntEnum):
    BUDGET = auto()
    FIXEDIE = auto()
    CATEGORY = auto()
    BALANCE = auto()
    LOCATION = auto()
    BACK = auto()

class SettingPage:
    
    errorMsg = "請輸入 1 到 6 之間的整數:"

    def show(self):
        print("%d: 查看/修改總預算" % SettingOption.BUDGET)
        print("%d: 新增每月固定收支" % SettingOption.FIXEDIE)
        print("%d: 查看/新增/修改/刪除類別" % SettingOption.CATEGORY)
        print("%d: 查看/新增/修改/刪除餘額" % SettingOption.BALANCE)
        print("%d: 查看/新增/修改/刪除地點" % SettingOption.LOCATION)
        print("%d: 回到上一頁" % SettingOption.BACK)
    
    def choose(self):
        while True:
            try:
                option = SettingOption(int(input()))
                break
            except ValueError:
                print(self.errorMsg)
        return option

    def enter(self, option):
        if option is SettingOption.BUDGET:
            nextPage = BudgetPage()
        elif option is SettingOption.FIXEDIE:
            nextPage = FixedIE()
        elif option is SettingOption.CATEGORY:
            nextPage = Category()
        elif option is SettingOption.BALANCE:
            nextPage = PaymentPage()
        elif option is SettingOption.LOCATION:
            nextPage = Location()
        else:
            raise ValueError(self.errorMsg)
        nextPage.start()

    def start(self):
        while True:
            self.show()
            option = self.choose()
            if option is SettingOption.BACK:
                return
            self.enter(option)
    
if __name__ == '__main__': # pragma: no cover
    settingsPage = SettingPage()
    settingsPage.start()