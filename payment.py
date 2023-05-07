from enum import IntEnum, auto
import sqlalchemy as sql
from accessor import Accessor

class PaymentOption(IntEnum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()
    BACK = auto()


class PaymentCategory(IntEnum):
    CASH = auto()
    DEBIT_CARD = auto()
    CREDIT_CARD = auto()
    ELECTRONIC = auto()
    OTHER = auto()


class Payment:
    name: str
    balance: int
    category: PaymentCategory


class PaymentPage(Accessor):

    table_name = "Payment"

    @staticmethod
    def show():
        print("%d: 新增支付方式" % PaymentOption.CREATE)
        print("%d: 查看支付方式" % PaymentOption.READ)
        print("%d: 修改支付方式" % PaymentOption.UPDATE)
        print("%d: 刪除支付方式" % PaymentOption.DELETE)
        print("%d: 回到上一頁" % PaymentOption.BACK)

    @staticmethod
    def choose():
        while True:
            try:
                option = PaymentOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 5 之間的數字:")
        return option

    @classmethod
    def execute(cls, option):
        if option is PaymentOption.CREATE:
            cls.create()
        elif option is PaymentOption.READ:
            cls.read()
        elif option is PaymentOption.UPDATE:
            cls.update()
        else:
            cls.delete()

    @classmethod
    def create(cls):
        cls.hint_create_name()
        name = input()
        cls.hint_create_balance()
        while True:
            try:
                balance = float(input())
                break
            except ValueError:
                print("請輸入數字:")
        cls.hint_create_category()
        while True:
            try:
                category = PaymentCategory(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 5 之間的數字:")
        cls.setUp_connection_and_table()
        query = cls.table.insert().values(name=name, balance=balance,category=category.name)
        rowsAffected = cls.conn.execute(query).rowcount
        cls.tearDown_connection()
        return rowsAffected == 1

    @staticmethod
    def hint_create_name():
        print("請輸入新支付方式的...")
        print("名稱:")

    @staticmethod
    def hint_create_balance():
        print("餘額:")

    @staticmethod
    def hint_create_category():
        print("類型(1 現金, 2 借記卡, 3 信用卡, 4 電子支付, 5 其他):")

    @classmethod
    def read(cls):
        cls.setUp_connection_and_table()
        query = sql.select(cls.table.c["name", "balance", "category"])
        results = cls.conn.execute(query).fetchall()
        cls.tearDown_connection()
        cls.format_print(results)
        
    @staticmethod
    def format_print(results):
        for row in results:
            dictRow = row._asdict()
            print("\"%s\" 剩餘 %s 元，支付類別為 %s" %(dictRow['name'], dictRow['balance'], dictRow['category']))

    def update(self, name, newName):
        pass

    @staticmethod
    def hint_update_original_name():
        print("請輸入要修改的支付方式的名稱:")
    
    @staticmethod
    def hint_update_option():
        print("請選擇要修改的項目(1 名稱, 2 餘額, 3 類別):")
    
    @staticmethod
    def hint_update_name():
        print("請選擇要修改的項目(1 名稱, 2 餘額, 3 類別):")

    @staticmethod
    def hint_update_balance():
        print("請選擇要修改的項目(1 名稱, 2 餘額, 3 類別):")

    @staticmethod
    def hint_update_category():
        print("請選擇要修改的項目(1 名稱, 2 餘額, 3 類別):")
    

    def delete(self, name):
        pass

    @classmethod
    def start(cls):
        while True:
            cls.show()
            option = cls.choose()
            if option is PaymentOption.BACK:
                return
            cls.execute(option)


if __name__ == "__main__":  # pragma: no cover
    PaymentPage.start()
