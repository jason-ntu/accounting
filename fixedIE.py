from enum import IntEnum, auto
import sqlalchemy as sql
from accessor import Accessor, ExecutionStatus as es
from datetime import datetime

class FixedIEOption(IntEnum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()
    BACK = auto()

class FixedIEUpdateOption(IntEnum):
    CATEGORY = auto()
    PAYMENT = auto()
    AMOUNT = auto()
    DAY = auto()
    NOTE = auto()
    BACK = auto()

class FixedIEType(IntEnum):
    INCOME = auto()
    EXPENSE = auto()

class CategoryOption(IntEnum):
    FOOD = auto()
    BEVERAGE = auto()
    OTHER = auto()

class PaymentOption(IntEnum):
    CASH = auto()
    DEBIT_CARD = auto()
    CREDIT_CARD = auto()
    ELECTRONIC = auto()
    OTHER = auto()

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
        else:
            cls.read()
            successful = cls.delete()
        if successful:
            cls.tearDown_connection(es.COMMIT)
        else:
            cls.tearDown_connection(es.ROLLBACK)

    @classmethod
    def create(cls):
        cls.hint_create_type()
        while True:
            try:
                IE = FixedIEType(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 2 之間的數字:")

        cls.hint_create_name(IE)
        name = input()

        # TODO: should read from "category"
        cls.hint_create_category()
        while True:
            try:
                category = CategoryOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 3 之間的數字:")

        # TODO: should read from "payment"
        cls.hint_create_payment()
        while True:
            try:
                payment = PaymentOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 5 之間的數字:")
        
        cls.hint_create_amount()
        while True:
            try:
                amount = float(input())
                break
            except ValueError:
                print("請輸入數字:")

        # TODO: should ask location

        cls.hint_create_day()
        while True:
            try:
                day = int(input())
                if day >= 1 and day <= 31:
                    break
                else:
                    print("請輸入 1 到 31 之間的數字:")
            except ValueError:
                print("請輸入 1 到 31 之間的數字:")

        cls.hint_create_note()
        note = input()

        query = cls.table.insert().values(IE=IE.name, name=name, category=category.name, payment=payment.name, amount=amount, day=day, note=note, flag=False)
        rowsAffected = cls.conn.execute(query).rowcount
        return rowsAffected == 1

    @staticmethod
    def hint_create_name(IE):
        if IE == FixedIEType.INCOME:
            print("請輸入新的固定收入名稱:")
        if IE == FixedIEType.EXPENSE:
            print("請輸入新的固定支出名稱:")

    @staticmethod
    def hint_create_amount():
        print("金額:")

    @staticmethod
    def hint_create_type():
        print("類型(1 固定收入, 2 固定支出):")

    @staticmethod
    def hint_create_category():
        print("記錄類別(1 食物, 2 飲料, 3 其他):")

    @staticmethod
    def hint_create_payment():
        print("收支方式(1 現金, 2 借記卡, 3 信用卡, 4 電子支付, 5 其他):")

    @staticmethod
    def hint_create_day():
        print("請輸入每月收支日(1-31):")

    @staticmethod
    def hint_create_note():
        print("請輸入備註:")

    @classmethod
    def read(cls):
        query = sql.select(cls.table.c['IE', 'name', 'category', 'payment', 'amount', 'day', 'note'])
        results = cls.conn.execute(query).fetchall()
        cls.format_print(results)

    @staticmethod
    def format_print(results):
        for row in results:
            dictRow = row._asdict()
            print("%s 名稱\"%s\" 類別%s 收支方式%s 金額%s 每月%s號 備註:%s" %(dictRow['IE'], dictRow['name'], dictRow['category'], dictRow['payment'], dictRow['amount'], dictRow['day'], dictRow['note']))

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
                    print("請輸入 1 到 6 之間的數字:",)

            if option == FixedIEUpdateOption.CATEGORY:
                return cls.update_category(name)
            elif option == FixedIEUpdateOption.PAYMENT:
                return cls.update_payment(name)
            elif option == FixedIEUpdateOption.AMOUNT:
                return cls.update_amount(name)
            elif option == FixedIEUpdateOption.DAY:
                return cls.update_day(name)
            elif option == FixedIEUpdateOption.NOTE:
                return cls.update_note(name)
            else:
                return True

    @staticmethod
    def hint_select_update_name():
        print("請輸入要修改的固定收支的名稱:")

    @staticmethod
    def hint_update_option():
        print("請選擇要修改的項目(1 類別, 2 收支方式, 3 金額, 4 時間, 5 備註, 6 返回):")

    @classmethod
    def update_category(cls, name):
        result = cls.conn.execute(cls.table.select().where(cls.table.c.name == name)).fetchone()
        original_category = result[2]

        cls.hint_update_category()
        while True:
            try:
                new_category = CategoryOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 3 之間的數字:")

        query = cls.table.update().where(cls.table.c.name == name).values(category=new_category.name)
        rowsAffected = cls.conn.execute(query).rowcount
        successful = (rowsAffected == 1)
        if not successful:
            return False
        else:
            print("名稱為 \"%s\" 的固定收支類別已成功更新為 %s" % (name, new_category.name))
            return True

    @staticmethod
    def hint_update_category():
        print("修改記錄類別為(1 食物, 2 飲料, 3 其他):")

    @classmethod
    def update_payment(cls, name):
        result = cls.conn.execute(cls.table.select().where(cls.table.c.name == name)).fetchone()
        original_payment = result[3]

        cls.hint_update_payment()
        while True:
            try:
                new_payment = PaymentOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 5 之間的數字:")

        query = cls.table.update().where(cls.table.c.name == name).values(payment=new_payment.name)
        rowsAffected = cls.conn.execute(query).rowcount
        successful = (rowsAffected == 1)
        if not successful:
            return False
        else:
            print("名稱為 \"%s\" 的固定收支方式已成功為 %s" % (name, new_payment.name))
            return True

    @staticmethod
    def hint_update_payment():
        print("修改收支方式為(1 現金, 2 借記卡, 3 信用卡, 4 電子支付, 5 其他):")

    @classmethod
    def update_amount(cls, name):
        result = cls.conn.execute(cls.table.select().where(cls.table.c.name == name)).fetchone()
        original_amount = result[4]

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
        successful = (rowsAffected == 1)
        if not successful:
            return False
        else:
            print("名稱為 \"%s\" 的固定收支金額已成功更新為 %.2f" % (name, new_amount))
            return True

    @staticmethod
    def hint_update_amount():
        print("修改金額為:")

    @staticmethod
    def hint_update_format_amount():
        print("請輸入大於0的數字:")

    @classmethod
    def update_day(cls, name):
        result = cls.conn.execute(cls.table.select().where(cls.table.c.name == name)).fetchone()
        original_day = result[5]

        cls.hint_update_day()
        while True:
            try:
                new_day = int(input())
                if new_day >= 1 and new_day <= 31:
                    break
                else:
                    print("請輸入 1 到 31 之間的數字:")
            except ValueError:
                print("請輸入 1 到 31 之間的數字:")

        query = cls.table.update().where(cls.table.c.name == name).values(day=new_day)
        rowsAffected = cls.conn.execute(query).rowcount
        successful = (rowsAffected == 1)
        if not successful:
            return False
        else:
            print("名稱為 \"%s\" 的固定收支時間已成功更新為每月 %d 號" % (name, new_day))
            return True

    @staticmethod
    def hint_update_day():
        print("修改每月收支日為(1-31):")

    @classmethod
    def update_note(cls, name):
        result = cls.conn.execute(cls.table.select().where(cls.table.c.name == name)).fetchone()
        original_note = result[6]

        cls.hint_update_note()
        new_note = input()

        query = cls.table.update().where(cls.table.c.name == name).values(note=new_note)
        rowsAffected = cls.conn.execute(query).rowcount
        successful = (rowsAffected == 1)
        if not successful:
            return False
        else:
            print("名稱為 \"%s\" 的固定收支備註已成功更新為%s" % (name, new_note))
            return True

    @staticmethod
    def hint_update_note():
        print("修改備註為:")

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
