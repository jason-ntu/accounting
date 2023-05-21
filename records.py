from enum import IntEnum, auto
from accessor import Accessor, ExecutionStatus as es
from category import CategoryPage
from payment import PaymentPage, PaymentCategory
from location import LocationPage

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
        elif option is RecordOption.DELETE:
            from deleteRecord import DeleteRecordPage
            DeleteRecordPage.start()
        # else:
        #     raise ValueError(cls.errorMsg)


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
    def showPayment(cls):
        for i in range(len(cls.paymentList)):
            print("%d %s(%s)" % (i+1, cls.paymentList[i]['name'], cls.paymentList[i]['category']))

    @classmethod
    def hintRetryPayment(cls):
        print("請輸入 1 到 %d 之間的數字:" % len(cls.paymentList))
    
    @classmethod
    def showLocation(cls):
        for i in range(len(cls.locationList)):
            print("%d %s" % (i+1, cls.locationList[i]))

    @classmethod
    def hintRetryLocation(cls):
        print("請輸入 1 到 %d 之間的數字:" % len(cls.locationList))

if __name__ == '__main__': # pragma: no cover
    RecordPage.start()
