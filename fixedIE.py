from enum import IntEnum, auto
import sqlalchemy as sql
from accessor import Accessor

class FixedIEOption(IntEnum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()
    BACK = auto()

class FixedIEUpdateOption(IntEnum):
    AMOUNT = auto()
    CATEGORY = auto()
    BACK = auto()

class FixedIECategory(IntEnum):
    INCOME = auto()
    EXPENSE = auto()

class FixedIE:
    name: str
    amount: int
    category: FixedIECategory


class FixedIEPage(Accessor):

    table_name = "FixedIE"

    @staticmethod
    def show():
        print("%d: 新增固定收支" % FixedIEOption.CREATE)
        print("%d: 查看固定收支" % FixedIEOption.READ)
        print("%d: 修改固定收支" % FixedIEOption.UPDATE)
        print("%d: 刪除固定收支" % FixedIEOption.DELETE)
        print("%d: 回到上一頁" % FixedIEOption.BACK)

    @staticmethod
    def choose():
        while True:
            try:
                option = FixedIEOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 5 之間的數字:")
        return option

    @classmethod
    def execute(cls, option):
        if option is FixedIEOption.CREATE:
            cls.create()
        elif option is FixedIEOption.READ:
            cls.read()
        elif option is FixedIEOption.UPDATE:
            cls.update()
        elif option is FixedIEOption.DELETE:
            cls.delete()

    @classmethod
    def create(cls):
        cls.hint_create_category()
        while True:
            try:
                category = FixedIECategory(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 2 之間的數字:")
        cls.hint_create_name(category)
        name = input()
        cls.hint_create_amount()
        while True:
            try:
                amount = float(input())
                break
            except ValueError:
                print("請輸入數字:")

        cls.setUp_connection_and_table()
        query = cls.table.insert().values(name=name, amount=amount, category=category.name)
        rowsAffected = cls.conn.execute(query).rowcount
        cls.tearDown_connection()
        return rowsAffected == 1

    @staticmethod
    def hint_create_name(category):
        if category == FixedIECategory.INCOME:
            print("請輸入新的固定收入")
        elif category == FixedIECategory.EXPENSE:
            print("請輸入新的固定支出")
        print("名稱:")

    @staticmethod
    def hint_create_amount():
        print("金額:")

    @staticmethod
    def hint_create_category():
        print("類型(1 固定收入, 2 固定支出):")

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
            print("固定收支: 名稱\"%s\" 金額%s 類別%s" %(dictRow['name'], dictRow['amount'], dictRow['category']))

    @classmethod
    def update(cls):
        cls.hint_select_update_name()
        name = input()
        cls.setUp_connection_and_table()
        query = cls.table.select().where(cls.table.c.name == name)
        result = cls.conn.execute(query)
        rows = result.fetchall()
        if len(rows) == 0:
            print("未找到名稱為 \"%s\" 的固定收支" % name)
        else:
            option = cls.select_update_option()
            if option == FixedIEUpdateOption.AMOUNT:
                cls.update_amount(name)
            elif option == FixedIEUpdateOption.CATEGORY:
                cls.update_category(name)
            elif option == FixedIEUpdateOption.BACK:
                pass
        cls.tearDown_connection()

    @staticmethod
    def hint_select_update_name():
        print("請輸入要修改的固定收支的名稱:")

    @staticmethod
    def select_update_option():
        print("請選擇要修改的項目：")
        print("1. 金額")
        print("2. 類別")
        print("3. 返回")
        while True:
            try:
                choice = int(input())
                if choice in [1, 2, 3]:
                    return FixedIEUpdateOption(choice)
                else:
                    print("請輸入 1 到 3 之間的數字")
            except ValueError:
                print("請輸入數字")

    @classmethod
    def update_amount(cls, name):
        result = cls.conn.execute(cls.table.select().where(cls.table.c.name == name)).fetchone()
        original_amount = result[1]
        cls.tearDown_connection()

        cls.hint_update_amount()
        new_amount = float(input())

        cls.setUp_connection_and_table()
        query = cls.table.update().where(cls.table.c.name == name).values(amount=new_amount)
        rowsAffected = cls.conn.execute(query).rowcount
        cls.tearDown_connection()

        if rowsAffected == 0:
            print("未更新任何資料")
        else:
            print("名稱為 \"%s\" 的固定收支金額已成功更新為 %.2f" % (name, new_amount))

    @staticmethod
    def hint_update_amount():
        print("修改金額為:")

    @classmethod
    def update_category(cls, name):
        result = cls.conn.execute(cls.table.select().where(cls.table.c.name == name)).fetchone()
        original_category = result[2]
        cls.tearDown_connection()

        cls.hint_update_category()
        while True:
            try:
                new_category = FixedIECategory(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 2 之間的數字:")

        cls.setUp_connection_and_table()
        query = cls.table.update().where(cls.table.c.name == name).values(category=new_category.name)
        rowsAffected = cls.conn.execute(query).rowcount
        cls.tearDown_connection()
        if rowsAffected == 0:
            print("未更新任何資料")
        else:
            print("名稱為 \"%s\" 的固定收支已成功更類別為 %d" % (name, new_category))

    @staticmethod
    def hint_update_category():
        print("修改類型為(1 固定收入, 2 固定支出):")

    @classmethod
    def delete(cls):
        cls.hint_delete_name()
        name = input()
        cls.setUp_connection_and_table()
        query = cls.table.delete().where(cls.table.c.name == name)
        rowsAffected = cls.conn.execute(query).rowcount
        cls.tearDown_connection()
        if rowsAffected == 0:
            print("未找到名稱為 \"%s\" 的固定收支" % name)
        else:
            print("名稱為 \"%s\" 的固定收支已成功刪除" % name)

    @staticmethod
    def hint_delete_name():
        print("請輸入要刪除的固定收支的名稱:")

    @classmethod
    def start(cls):
        while True:
            cls.show()
            option = cls.choose()
            if option is FixedIEOption.BACK:
                return
            cls.execute(option)

if __name__ == "__main__":  # pragma: no cover
    FixedIEPage.start()
