from enum import IntEnum, auto
import sqlalchemy as sql
from accessor import Accessor, ExecutionStatus as es
import const

class AccountOption(IntEnum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()
    BACK = auto()

class AccountUpdateOption(IntEnum):
    NAME = auto()
    BALANCE = auto()
    CATEGORY = auto()

class AccountCategory(IntEnum):
    CASH = auto()
    DEBIT_CARD = auto()
    CREDIT_CARD = auto()
    ELECTRONIC = auto()
    OTHER = auto()

class AccountPage(Accessor):

    table_name = "Account"

    @staticmethod
    def show():
        print("%d: 新增支付方式" % AccountOption.CREATE)
        print("%d: 查看支付方式" % AccountOption.READ)
        print("%d: 修改支付方式" % AccountOption.UPDATE)
        print("%d: 刪除支付方式" % AccountOption.DELETE)
        print("%d: 回到上一頁" % AccountOption.BACK)

    @staticmethod
    def choose():
        while True:
            try:
                option = AccountOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 5 之間的數字:")
        return option

    @classmethod
    def execute(cls, option):
        cls.setUp_connection_and_table()
        if option is AccountOption.CREATE:
            successful = cls.create()
        elif option is AccountOption.READ:
            cls.read()
            cls.tearDown_connection(es.NONE)
            return
        elif option is AccountOption.UPDATE:
            successful = cls.update()
        else:
            successful = cls.delete()
        if successful:
            cls.tearDown_connection(es.COMMIT)
        else:
            cls.tearDown_connection(es.ROLLBACK)

    @classmethod
    # TODO Handle the case that the name is not unique
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
                category = AccountCategory(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 5 之間的數字:")
        query = cls.table.insert().values(name=name, balance=balance,category=category.name)
        rowsAffected = cls.conn.execute(query).rowcount
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
        query = sql.select(cls.table.c["name", "balance", "category"])
        results = cls.conn.execute(query).fetchall()
        for row in results:
            dictRow = row._asdict()
            print("\"%s\" 剩餘 %s 元，支付類型為 %s" %(dictRow['name'], dictRow['balance'], dictRow['category']))
        
    @classmethod
    # TODO Handle the case that the name doen't exist
    # TODO Handle the case that the update is the saem as the original
    def update(cls):
        cls.hint_update_name()
        name = input()
        cls.hint_update_option()
        while True:
            try:
                option = AccountUpdateOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 3 之間的數字:")
        if option is AccountUpdateOption.NAME:
            cls.hint_update_new_name()
            newName = input()
            query = cls.table.update().values(name=newName).where(cls.table.c.name == name)
        elif option is AccountUpdateOption.BALANCE:
            cls.hint_update_new_balance()
            while True:
                try:
                    newBalance = float(input())
                    break
                except ValueError:
                    print("請輸入數字:")
            query = cls.table.update().values(balance=newBalance).where(cls.table.c.name == name)
        else:
            cls.hint_update_new_category()
            while True:
                try:
                    newCategory = AccountCategory(int(input()))
                    break
                except ValueError:
                    print("請輸入 1 到 5 之間的數字:")
            query = cls.table.update().values(category=newCategory.name).where(cls.table.c.name == name)
        rowsAffected = cls.conn.execute(query).rowcount
        if rowsAffected > 1:
            print("%s%s 對應到多個支付方式%s" % (const.ANSI_YELLOW, name, const.ANSI_RESET))
            return False
        elif rowsAffected == 0:
            print("%s%s 對應不到任何支付方式%s" % (const.ANSI_YELLOW, name, const.ANSI_RESET))
            return False
        else:
            return True

    @staticmethod
    def hint_update_name():
        print("請輸入要修改的支付方式名稱:")
    
    @staticmethod
    def hint_update_option():
        print("請選擇要修改的項目(1 名稱, 2 餘額, 3 類型):")
    
    @staticmethod
    def hint_update_new_name():
        print("請輸入新的名稱:")

    @staticmethod
    def hint_update_new_balance():
        print("請輸入新的餘額:")

    @staticmethod
    def hint_update_new_category():
        print("請輸入新的類型(1 現金, 2 借記卡, 3 信用卡, 4 電子支付, 5 其他):")
    
    @classmethod
    def delete(cls):
        cls.hint_delete()
        name = input()
        query = cls.table.delete().where(cls.table.c.name == name)
        rowsAffected = cls.conn.execute(query).rowcount
        if rowsAffected == 0:
            print("%s%s 對應不到任何支付方式%s" % (const.ANSI_YELLOW, name, const.ANSI_RESET))
            return False
        return True

    def hint_delete():
        print("請輸入要刪除的支付方式名稱:")

    @classmethod
    def start(cls):
        while True:
            cls.show()
            option = cls.choose()
            if option is AccountOption.BACK:
                return
            cls.execute(option)

    @classmethod
    def getList(cls):
        cls.setUp_connection_and_table()
        query = sql.select(cls.table.c['name', 'category'])
        results = cls.conn.execute(query).fetchall()
        cls.tearDown_connection(es.NONE)
        accountList = []
        for row in results:
            dictRow = row._asdict()
            accountList.append(dictRow)
        return accountList
