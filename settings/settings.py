from structure import SettingsOption
from .budget import Budget
from .fixedIE import FixedIE
from .category import Category
from .balance import Balance
from .location import Location

class SettingsPage:
    def show(self):
        print("%d: 查看/修改總預算" % SettingsOption.BUDGET)
        print("%d: 新增每月固定收支" % SettingsOption.FIXEDIE)
        print("%d: 查看/新增/修改/刪除類別" % SettingsOption.CATEGORY)
        print("%d: 查看/新增/修改/刪除餘額" % SettingsOption.BALANCE)
        print("%d: 查看/新增/修改/刪除地點" % SettingsOption.LOCATION)
    
    def choose(self):
        while True:
            try:
                option = int(input())
                if option == 0 or option > 5:
                    raise ValueError
                break
            except ValueError:
                print('請輸入 1 到 5 之間的數字 (inclusive):')
        return option

    def enter(self, option):
        if option == SettingsOption.BUDGET:
            Budget.start()
        elif option == SettingsOption.FIXEDIE:
            FixedIE.start()
        elif option == SettingsOption.CATEGORY:
            Category.start()
        elif option == SettingsOption.BALANCE:
            Balance.start()
        elif option == SettingsOption.LOCATION:
            Location.start()
        else:
            raise ValueError

    def start(self):
        self.show()
        option = self.choose()
        self.enter(option)
    
if __name__ == '__main__': # pragma: no cover
    settingsPage = SettingsPage()
    settingsPage.start()