from enum import IntEnum, auto
import sqlalchemy as sql
from accessor import Accessor

class IncomeOption(IntEnum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()
    BACK = auto()


class IncomeCategory(IntEnum):
    SALARY = auto()
    BONUS = auto()
    INVESTMENT = auto()
    OTHER = auto()


class Income:
    name: str
    amount: int
    category: IncomeCategory


class IncomePage(Accessor):

    table_name = "Income"

    @staticmethod
    def show():
        print("%d: 新增收入方式" % IncomeOption.CREATE)
        print("%d: 查看收入方式" % IncomeOption.READ)
        print("%d: 修改收入方式" % IncomeOption.UPDATE)
        print("%d: 刪除收入方式" % IncomeOption.DELETE)
        print("%d: 回到上一頁" % IncomeOption.BACK)

    @staticmethod
    def choose():
        while True:
            try:
                option = IncomeOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 5 之間的數字:")
        return option

    @classmethod
    def execute(cls, option):
        if option is IncomeOption.CREATE:
            cls.create()
        elif option is IncomeOption.READ:
            cls.read()
        elif option is IncomeOption.UPDATE:
            cls.update()
        elif option is IncomeOption.DELETE:
            cls.delete()

    @classmethod
    def create(cls):
        cls.hint_create_name()
        name = input()
        cls.hint_create_amount()
        while True:
            try:
                amount = float(input())
                break
            except ValueError:
                print("請輸入數字:")
        cls.hint_create_category()
        while True:
            try:
                category = IncomeCategory(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 4 之間的數字:")
        cls.setUp_connection_and_table()
        query = cls.table.insert().values(name=name, amount=amount, category=category.name)
        rowsAffected = cls.conn.execute(query).rowcount
        cls.tearDown_connection()
        return rowsAffected == 1

    @staticmethod
    def hint_create_name():
        print("請輸入新收入方式的...")
        print("名稱:")

    @staticmethod
    def hint_create_amount():
        print("金額:")

    @staticmethod
    def hint_create_category():
        print("類型(1 薪資, 2 獎金, 3 投資收益, 4 其他):")

    @classmethod
    def read(cls):
        cls.setUp_connection_and_table()
        query = sql.select(cls.table.c["name", "amount", "category"])
        results = cls.conn.execute(query).fetchall()
        cls.tearDown_connection()
        cls.format_print(results)

    @staticmethod
    def format_print(results):
        for row in results:
            dictRow = row._asdict()
            print("\"%s\" 獲得 %s 元，收入類別為 %s" %(dictRow['name'], dictRow['amount'], dictRow['category']))

    @classmethod
    def update(cls):
        cls.hint_update_original_name()
        name = input()
        cls.hint_update_new_name()
        updatedName = input()
        cls.setUp_connection_and_table()
        query = cls.table.update().where(cls.table.c.name == name).values(name=updatedName)
        rowsAffected = cls.conn.execute(query).rowcount
        cls.tearDown_connection()
        if rowsAffected == 0:
            print("未找到名稱為 \"%s\" 的收入項目" % name)
        else:
            print("名稱為 \"%s\" 的收入項目已成功更新為 \"%s\"" % (name, updatedName))

    @staticmethod
    def hint_update_original_name():
        print("請輸入要修改的收入項目的名稱:")

    @staticmethod
    def hint_update_new_name():
        print("修改收入項目的名稱為:")

    @classmethod
    def delete(cls):
        cls.hint_delete_name()
        name = input()
        cls.setUp_connection_and_table()
        query = cls.table.delete().where(cls.table.c.name == name)
        rowsAffected = cls.conn.execute(query).rowcount
        cls.tearDown_connection()
        if rowsAffected == 0:
            print("未找到名稱為 \"%s\" 的收入項目" % name)
        else:
            print("名稱為 \"%s\" 的收入項目已成功刪除" % name)

    @staticmethod
    def hint_delete_name():
        print("請輸入要刪除的收入項目的名稱:")

    @classmethod
    def start(cls):
        while True:
            cls.show()
            option = cls.choose()
            if option is IncomeOption.BACK:
                return
            cls.execute(option)

if __name__ == "__main__":  # pragma: no cover
    IncomePage.start()
