from enum import IntEnum, auto
import utils


class BudgetOption(IntEnum):
    READ = auto()
    UPDATE = auto()
    BACK = auto()


class BudgetPage:
    @staticmethod
    def show():
        print("%d: 查看總預算" % BudgetOption.READ)
        print("%d: 修改總預算" % BudgetOption.UPDATE)
        print("%d: 回到上一頁" % BudgetOption.BACK)

    @staticmethod
    def choose():
        while True:
            try:
                option = BudgetOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 3 之間的數字:")
        return option

    @classmethod
    def execute(cls, option):
        if option is BudgetOption.READ:
            cls.read()
        else:
            cls.update()

    @staticmethod
    def read():
        budget = utils.db_read("""SELECT `amount` FROM `budget_table` WHERE id='1'""")
        return budget[0]["amount"]

    @classmethod
    def update(cls):
        cls.hint_update()
        while True:
            try:
                newAmount = float(input())
                return utils.db_write(
                    """UPDATE `budget_table` SET `amount`='%f' WHERE id='1'"""
                    % newAmount
                )
            except ValueError:
                print("請輸入數字:")

    @staticmethod
    def hint_update():
        print("請輸入新的總預算:")

    @classmethod
    def start(cls):
        while True:
            cls.show()
            option = cls.choose()
            if option is BudgetOption.BACK:
                return
            cls.execute(option)


if __name__ == "__main__":  # pragma: no cover
    BudgetPage.start()
