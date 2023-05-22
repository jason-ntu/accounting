from enum import IntEnum, auto
from accessor import Accessor
from category import CategoryPage
from account import AccountPage
from location import LocationPage
from datetime import datetime
import re

# 消費紀錄 Records
# > 新增消費紀錄
# > 檢視消費紀錄 
# > 修改消費紀錄
# > 刪除消費紀錄

class RecordOption(IntEnum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()
    BACK = auto()

class RecordPage(Accessor):

    table_name = "Record"
    IEList = ["INCOME", "EXPENSE"]
    categoryList = []
    accountList = []
    locationList = []
    
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
        elif option is RecordOption.DELETE:
            from deleteRecord import DeleteRecordPage
            DeleteRecordPage.start()
        # else:
        #     raise ValueError(cls.errorMsg)

    @classmethod
    def askIE(cls):
        cls.hintGetIE()
        while True:
            try:
                IE = int(input())
                if IE <= len(cls.IEList):
                    break
                else: 
                    raise ValueError()
            except ValueError:
                cls.hintGetIE()
        return IE

    @classmethod
    def askCategory(cls):
        cls.categoryList = CategoryPage.getList()
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
    def showCategory(cls):
        for i in range(len(cls.categoryList)):
            print("%d %s" % (i+1, cls.categoryList[i]))
    
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
    def showAccount(cls):
        for i in range(len(cls.accountList)):
            print("%d %s(%s)" % (i+1, cls.accountList[i]['name'], cls.accountList[i]['category']))

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
        cls.locationList = LocationPage.getList()
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
    def showLocation(cls):
        for i in range(len(cls.locationList)):
            print("%d %s" % (i+1, cls.locationList[i]))

    @classmethod
    def hintRetryLocation(cls):
        print("請輸入 1 到 %d 之間的數字:" % len(cls.locationList))
    
    @staticmethod
    def hintNumberErorMsg():
        print("請輸入數字")

    @classmethod
    def askPurchaseDate(cls):
        cls.hintGetPurchaseDate()
        while True:
            try:
                date = cls.askDate()
                break
            except ValueError:
                cls.hintGetPurchaseDate()
        return date
    
    @classmethod
    def askDebitDate(cls):
        cls.hintGetDebitDate()
        while True:
            try:
                date = cls.askDate()
                break
            except ValueError:
                cls.hintGetDebitDate()
        return date
    
    @classmethod
    def askDate(cls):
        date = input()
        if (date == ""):
            date = datetime.today().date()
        else:
            datetime.strptime(date, '%Y-%m-%d').date()
        return date

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

if __name__ == '__main__': # pragma: no cover
    RecordPage.start()
