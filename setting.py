from enum import IntEnum, auto
from accessor import Accessor
from budget import BudgetPage
from fixedIE import FixedIEPage
from category import CategoryPage
from payment import PaymentPage
from location import LocationPage


class SettingOption(IntEnum):
    BUDGET = auto()
    FIXEDIE = auto()
    CATEGORY = auto()
    BALANCE = auto()
    LOCATION = auto()
    BACK = auto()


class SettingPage():
    @staticmethod
    def show():
        print("%d: 查看/修改總預算" % SettingOption.BUDGET)
        print("%d: 查看/新增每月固定收支" % SettingOption.FIXEDIE)
        print("%d: 查看/新增/修改/刪除類別" % SettingOption.CATEGORY)
        print("%d: 查看/新增/修改/刪除支付方式" % SettingOption.BALANCE)
        print("%d: 查看/新增/修改/刪除地點" % SettingOption.LOCATION)
        print("%d: 回到上一頁" % SettingOption.BACK)

    @staticmethod
    def choose():
        while True:
            try:
                option = SettingOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 6 之間的整數:")
        return option

    @staticmethod
    def execute(option):
        if option is SettingOption.BUDGET:
            BudgetPage.start()
        elif option is SettingOption.FIXEDIE:
            FixedIEPage.start()
        elif option is SettingOption.CATEGORY:
            CategoryPage.start()
        elif option is SettingOption.BALANCE:
            PaymentPage.start()
        else:
            LocationPage.start()

    @classmethod
    def start(cls):
        while True:
            cls.show()
            option = cls.choose()
            if option is SettingOption.BACK:
                return
            cls.execute(option)


if __name__ == "__main__":  # pragma: no cover
    SettingPage.start()
