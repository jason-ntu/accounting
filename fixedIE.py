from enum import IntEnum, auto
import sqlalchemy as sql
from accessor import Accessor, ExecutionStatus as es

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
        print("[固定收支設定]")
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
        cls.setUp_connection_and_table()
        if option is FixedIEOption.CREATE:
            successful = cls.create()
        elif option is FixedIEOption.READ:
            cls.read()
            cls.tearDown_connection(es.NONE)
            return
        elif option is FixedIEOption.UPDATE:
            cls.read()
            successful = cls.update()
        else: # option is FixedIEOption.DELETE:
            cls.read()
            successful = cls.delete()
        if successful:
            cls.tearDown_connection(es.COMMIT)
        else:
            cls.tearDown_connection(es.ROLLBACK)

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

        query = cls.table.insert().values(name=name, amount=amount, category=category.name)
        rowsAffected = cls.conn.execute(query).rowcount
        return rowsAffected == 1

    @staticmethod
    def hint_create_name(category):
        if category == FixedIECategory.INCOME:
            print("請輸入新的固定收入...")
        if category == FixedIECategory.EXPENSE:
            print("請輸入新的固定支出...")
        print("名稱:")

    @staticmethod
    def hint_create_amount():
        print("金額:")

    @staticmethod
    def hint_create_category():
        print("類型(1 固定收入, 2 固定支出):")

    @classmethod
    def read(cls):
        query = sql.select(cls.table.c["name", "amount", "category"])
        results = cls.conn.execute(query).fetchall()
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
        query = cls.table.select().where(cls.table.c.name == name)
        result = cls.conn.execute(query)
        rows = result.fetchall()
        if len(rows) == 0:
            print("未找到名稱為 \"%s\" 的固定收支" % name)
        else:
            cls.hint_update_option()
            while True:
                try:
                    option = FixedIEUpdateOption(int(input()))
                    break
                except ValueError:
                    print("請輸入 1 到 3 之間的數字")

            if option == FixedIEUpdateOption.AMOUNT:
                return cls.update_amount(name)
            elif option == FixedIEUpdateOption.CATEGORY:
                return cls.update_category(name)
            else: # option == FixedIEUpdateOption.BACK:
                return True

    @staticmethod
    def hint_select_update_name():
        print("請輸入要修改的固定收支的名稱:")

    @staticmethod
    def hint_update_option():
        print("請選擇要修改的項目(1 金額, 2 類別, 3 返回):")

    @classmethod
    def update_amount(cls, name):
        result = cls.conn.execute(cls.table.select().where(cls.table.c.name == name)).fetchone()
        original_amount = result[1]

        cls.hint_update_amount()
        while True:
            try:
                new_amount = float(input())
                if new_amount <= 0:
                    cls.hint_update_format_amount()
                else:
                    break
            except:
                cls.hint_update_format_amount()

        query = cls.table.update().where(cls.table.c.name == name).values(amount=new_amount)
        rowsAffected = cls.conn.execute(query).rowcount

        print("名稱為 \"%s\" 的固定收支金額已成功更新為 %.2f" % (name, new_amount))
        return True

    @staticmethod
    def hint_update_amount():
        print("修改金額為:")

    @staticmethod
    def hint_update_format_amount():
        print("請輸入大於0的數字:")

    @classmethod
    def update_category(cls, name):
        result = cls.conn.execute(cls.table.select().where(cls.table.c.name == name)).fetchone()
        original_category = result[2]

        cls.hint_update_category()
        while True:
            try:
                new_category = FixedIECategory(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 2 之間的數字:")

        query = cls.table.update().where(cls.table.c.name == name).values(category=new_category.name)
        rowsAffected = cls.conn.execute(query).rowcount
        print("名稱為 \"%s\" 的固定收支已成功更類別為 %s" % (name, new_category.name))
        return True

    @staticmethod
    def hint_update_category():
        print("修改類型為(1 固定收入, 2 固定支出):")

    @classmethod
    def delete(cls):
        cls.hint_delete_name()
        name = input()
        query = cls.table.delete().where(cls.table.c.name == name)
        rowsAffected = cls.conn.execute(query).rowcount
        if rowsAffected == 0:
            print("未找到名稱為 \"%s\" 的固定收支" % name)
            return False
        else:
            print("名稱為 \"%s\" 的固定收支已成功刪除" % name)
            return True

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
