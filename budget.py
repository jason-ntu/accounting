from enum import IntEnum, auto
import utils

class BudgetOption(IntEnum):
    READ = auto()
    UPDATE = auto()
    BACK = auto()

class BudgetPage:

    errorMsg = "請輸入 1 到 3 之間的數字:"

    def show(self):
        print("%d: 查看總預算" % BudgetOption.READ)
        print("%d: 修改總預算" % BudgetOption.UPDATE)
        print("%d: 回到上一頁" % BudgetOption.BACK)

    def choose(self):
        while True:
            try:
                option = BudgetOption(int(input()))
                break
            except ValueError:
                print(self.errorMsg)
        return option

    def execute(self,option):
        if option is BudgetOption.READ:
            self.read()
        elif option is BudgetOption.UPDATE:
            self.update()
        else:
            raise ValueError(self.errorMsg)

    def read(self):
        budget = utils.db_read("""SELECT `int` FROM `budget_table` WHERE id='1'""")
        return budget[0]['int']

    def update(self):
        self.hint()
        while True:
            try:
                return utils.db_write("""UPDATE `budget_table` SET `int`='%d' WHERE id='1'""" % int(input()))
            except ValueError:
                print("請輸入整數")

    def hint(self):
        print("請輸入新的總預算:")

    def start(self):
        while True:
            self.show()
            option = self.choose()
            if option is BudgetOption.BACK:
                return
            self.execute(option)

if __name__ == '__main__':  # pragma: no cover
    budgetPage = BudgetPage()
    budgetPage.start()