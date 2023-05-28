from enum import IntEnum, auto
from accessor import Accessor
from category import CategoryPage
from account import AccountPage
from location import LocationPage
from datetime import datetime
from accessor import ExecutionStatus as es
from IEDirection import IEDirection
import sqlalchemy as sql
import re

class RecordOption(IntEnum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()
    BACK = auto()

class RecordPage(Accessor):

    table_name = "Record"
    categoryList = []
    accountList = []
    locationList = []
    IE = ""
    
    @staticmethod
    def choose():
        while True:
            try:
                option = RecordOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 5 之間的數字:")
        return option

    @classmethod
    def start(clf):
        while True:
            clf.show()
            option = clf.choose()
            if option is RecordOption.BACK:
                return
            clf.execute(option)

    @staticmethod
    def show():
        print("%d: 新增消費紀錄" % RecordOption.CREATE)
        print("%d: 檢視消費紀錄" % RecordOption.READ)
        print("%d: 修改消費紀錄" % RecordOption.UPDATE)
        print("%d: 刪除消費紀錄" % RecordOption.DELETE)
        print("%d: 回到上一頁" % RecordOption.BACK)

    @classmethod
    def execute(cls, option):
        if option is RecordOption.CREATE:
            from createRecord import CreateRecordPage
            CreateRecordPage.start()
        elif option is RecordOption.READ:
            from readRecord import ReadRecordPage
            ReadRecordPage.start()
        elif option is RecordOption.UPDATE:
            from updateRecord import UpdateRecordPage
            UpdateRecordPage.start()
        else: 
            from deleteRecord import DeleteRecordPage
            DeleteRecordPage.start()

    @classmethod
    def askCategory(cls):
        cls.categoryList = CategoryPage.getList(cls.IE)
        cls.showCategory()
        cls.hintGetCategory()
        while True:
            try:
                choice = int(input())
                if choice not in range(1, len(cls.categoryList)+1):
                    raise ValueError
                category = cls.categoryList[choice-1]
                break
            except ValueError:
                cls.hintRetryCategory()
        return category
    
    @classmethod
    def askIE(cls):
        cls.hintGetIE()
        while True:
            try:
                IE = IEDirection(int(input()))
                break
            except ValueError:
                cls.hintGetIE()
        return IE

    @classmethod
    def showCategory(cls): # pragma: no cover
        for i, category in enumerate(cls.categoryList, 1):
            print(f"{i} {category}")
    
    @classmethod
    def hintRetryCategory(cls):
        print("請輸入 1 到 %d 之間的數字:" % len(cls.categoryList))
    
    @classmethod
    def askAccount(cls):
        cls.accountList = AccountPage.getList()
        cls.showAccount()
        cls.hintGetAccount()
        while True:
            try:
                choice = int(input())
                if choice not in range(1, len(cls.accountList)+1):
                    raise ValueError
                account = cls.accountList[choice-1]
                break
            except ValueError:
                cls.hintRetryAccount()
        return account

    @classmethod
    def showAccount(cls): # pragma: no cover
        for i, account in enumerate(cls.accountList, 1):
            print(f"{i} {account['name']}({account['category']})")

    @classmethod
    def hintRetryAccount(cls):
        print("請輸入 1 到 %d 之間的數字:" % len(cls.accountList))
    
    @classmethod
    def askAmount(cls):
        cls.hintGetAmount()
        while True:
            try:
                amount = float(input())
                if amount <= 0:
                    raise ValueError
                else:
                    break
            except ValueError:
                cls.hintNumberErorMsg()
        return amount

    @staticmethod
    def hintRetryAmount():
        print("請輸入大於0的數字:")

    @classmethod
    def askLocation(cls):
        cls.locationList = LocationPage.getList(cls.IE)
        cls.showLocation()
        cls.hintGetLocation()
        while True:
            try:
                choice = int(input())
                if choice not in range(1, len(cls.locationList)+1):
                    raise ValueError
                location = cls.locationList[choice-1]
                break
            except ValueError:
                cls.hintRetryLocation()
        return location

    @classmethod
    def showLocation(cls): # pragma: no cover
        for i, location in enumerate(cls.locationList, 1):
            print(f"{i} {location}")
    
    @classmethod
    def askPurchaseDate(cls):
        cls.hintGetPurchaseDate()
        while True:
            try:
                Date = input()
                if Date == "":
                    Date = datetime.today().date()
                    break
                else:
                    datetime.strptime(Date, '%Y-%m-%d').date()
                    break
            except ValueError:
                cls.hintGetPurchaseDate()
        return Date

    @classmethod
    def askDebitDate(cls):
        cls.hintGetDebitDate()
        while True:
            try:
                Date = input()
                if Date == "":
                    Date = datetime.today().date()
                    break
                else:
                    datetime.strptime(Date, '%Y-%m-%d').date()
                    break
            except ValueError:
                cls.hintGetDebitDate()
        return Date
    
    @classmethod
    def askInvoice(cls):
        cls.hintGetInvoice()
        invoice = input()
        while invoice != "":
            try:
                pattern = r'\d{8}$'
                match = re.match(pattern, invoice)
                if match:
                    break
                else:
                    raise ValueError()
            except ValueError:
                cls.hintGetInvoice()
                invoice = input()
        return invoice

    @classmethod
    def askNote(cls):
        cls.hintGetNote()
        note = input()
        return note
    
    @classmethod
    def updateAccountAmount(cls, IE, account_name, amount):
        if (IE == "EXPENSE"):
            amount *= -1
        query_balance = sql.select(cls.tables[1].c['balance']).where(cls.tables[1].c.name == account_name)
        account = cls.conn.execute(query_balance).fetchone()
        dictAccount = account._asdict() 
        originAmount = dictAccount['balance']
        newAmount = originAmount + amount
        update_balance = sql.update(cls.tables[1]).where(cls.tables[1].c.name == account_name).values(balance=newAmount)
        resultProxy = cls.conn.execute(update_balance)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("更新帳戶餘額失敗")
            cls.tearDown_connection(es.ROLLBACK)
            return
        cls.tearDown_connection(es.COMMIT)
    
    @classmethod
    def hintRetryLocation(cls):
        print("請輸入 1 到 %d 之間的數字:" % len(cls.locationList))
    
    @staticmethod
    def hintNumberErorMsg():
        print("請輸入數字:")
    
    @staticmethod
    def hintGetCategory():
        print("請輸入紀錄類型:")
    
    @staticmethod
    def hintGetAmount():
        print("請輸入金額:")

    @staticmethod
    def hintGetLocation():
        print("請輸入消費地點:")

    @staticmethod
    def hintGetPurchaseDate():
        print("請輸入消費日期(yyyy-mm-dd):")

    @staticmethod
    def hintGetDebitDate():
        print("請輸入扣款日期(yyyy-mm-dd):")

    @staticmethod
    def hintGetNote():
        print("請輸入備註:")

    @staticmethod
    def hintGetInvoice():
        print("請輸入發票末八碼數字:")
    
    @staticmethod
    def hintGetAccount():
        print("請輸入帳戶:")
    
    @staticmethod
    def hintGetIE():
        print("1 收入 2 支出")
        print("請選擇新的收入/支出:")
    

if __name__ == '__main__': # pragma: no cover
    RecordPage.start()
