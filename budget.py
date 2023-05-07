from enum import IntEnum, auto
import sqlalchemy as sql
from accessor import Accessor, ExecutionStatus as es


class BudgetOption(IntEnum):
    READ = auto() 
    UPDATE = auto()
    BACK = auto()


class BudgetPage(Accessor):

    table_name = "Budget"

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

    @classmethod
    def read(cls):
        cls.setUp_connection_and_table()
        query = sql.select(cls.table.c["amount"])
        result = cls.conn.execute(query).first()
        cls.tearDown_connection(es.ROLLBACK)
        print(result._asdict()['amount'])

    @classmethod
    def update(cls):
        cls.hint_update()
        while True:
            try:
                newAmount = float(input())
                break
            except ValueError:
                print("請輸入數字:")
        cls.setUp_connection_and_table()
        query = cls.table.update().values(amount=newAmount).where(cls.table.c.id == 1)
        rowsAffected = cls.conn.execute(query).rowcount
        cls.tearDown_connection(es.COMMIT)
        return rowsAffected == 1

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
