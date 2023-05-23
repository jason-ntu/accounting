from enum import IntEnum, auto
from accessor import Accessor
from category import CategoryPage
from payment import PaymentPage
from location import LocationPage
from datetime import datetime
import re

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
    paymentList = []
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
        else: 
            from deleteRecord import DeleteRecordPage
            DeleteRecordPage.start()

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
    def showCategory(cls): # pragma: no cover
        for i in range(len(cls.categoryList)):
            print("%d %s" % (i+1, cls.categoryList[i]))
    
    @classmethod
    def hintRetryCategory(cls):
        print("請輸入 1 到 %d 之間的數字:" % len(cls.categoryList))
    
    @classmethod
    def askPayment(cls):
        cls.paymentList = PaymentPage.getList()
        cls.showPayment()
        cls.hintGetPayment()
        while True:
            try:
                choice = int(input())
                if choice not in range(1, len(cls.paymentList)+1):
                    raise ValueError
                payment = cls.paymentList[choice-1]
                break
            except ValueError:
                cls.hintRetryPayment()
        return payment

    @classmethod
    def showPayment(cls): # pragma: no cover
        for i in range(len(cls.paymentList)):
            print("%d %s(%s)" % (i+1, cls.paymentList[i]['name'], cls.paymentList[i]['category']))

    @classmethod
    def hintRetryPayment(cls):
        print("請輸入 1 到 %d 之間的數字:" % len(cls.paymentList))
    
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
    def showLocation(cls): # pragma: no cover
        for i in range(len(cls.locationList)):
            print("%d %s" % (i+1, cls.locationList[i]))
    
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
    def hintRetryLocation(cls):
        print("請輸入 1 到 %d 之間的數字:" % len(cls.locationList))
    
    @staticmethod
    def hintNumberErorMsg():
        print("請輸入數字:")
    
    @staticmethod
    def hintGetCategory():
        print("請輸入紀錄類型:")

    @staticmethod
    def hintGetPayment():
        print("請輸入收支方式:")
    
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

if __name__ == '__main__': # pragma: no cover
    RecordPage.start()
