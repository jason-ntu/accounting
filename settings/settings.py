from enum import IntEnum, auto
from settings.budget import BudgetPage
from settings.fixedIE import FixedIE
from settings.category import Category
from settings.balance import Balance
from settings.location import Location

class SettingsOption(IntEnum):
    BUDGET = auto()
    FIXEDIE = auto()
    CATEGORY = auto()
    BALANCE = auto()
    LOCATION = auto()
    BACK = auto()

class SettingsPage:
    
    errorMsg = "請輸入 1 到 6 之間的數字:"

    def show(self):
        print("%d: 查看/修改總預算" % SettingsOption.BUDGET)
        print("%d: 新增每月固定收支" % SettingsOption.FIXEDIE)
        print("%d: 查看/新增/修改/刪除類別" % SettingsOption.CATEGORY)
        print("%d: 查看/新增/修改/刪除餘額" % SettingsOption.BALANCE)
        print("%d: 查看/新增/修改/刪除地點" % SettingsOption.LOCATION)
        print("%d: 回到上一頁" % SettingsOption.BACK)
    
    def choose(self):
        while True:
            try:
                option = SettingsOption(int(input()))
                break
            except ValueError:
                print(self.errorMsg)
        return option

    def enter(self, option):
        if option is SettingsOption.BUDGET:
            nextPage = BudgetPage()
        elif option is SettingsOption.FIXEDIE:
            nextPage = FixedIE()
        elif option is SettingsOption.CATEGORY:
            nextPage = Category()
        elif option is SettingsOption.BALANCE:
            nextPage = Balance()
        elif option is SettingsOption.LOCATION:
            nextPage = Location()
        else:
            raise ValueError(self.errorMsg)
        nextPage.start()

    def start(self):
        while True:
            self.show()
            option = self.choose()
            if option is SettingsOption.BACK:
                return
            self.enter(option)
    
if __name__ == '__main__': # pragma: no cover
    settingsPage = SettingsPage()
    settingsPage.start()