from enum import IntEnum, auto
from accessor import Accessor, ExecutionStatus as es
import sqlalchemy as sql
import sys
from datetime import datetime
import re
from fixedIE import FixedIEType
from category import CategoryPage
from payment import PaymentPage, PaymentCategory
from location import LocationPage
from records import RecordPage


class CreateRecordOption(IntEnum):
    INCOME = auto()
    EXPENSE = auto()
    BACK = auto()

class CreateRecordPage(RecordPage):

    IE = ""

    @staticmethod
    def show():
        print("%d: 新增收入" % CreateRecordOption.INCOME)
        print("%d: 新增支出" % CreateRecordOption.EXPENSE)
        print("%d: 回到上一頁" % CreateRecordOption.BACK)

    @staticmethod
    def choose():
        while True:
            try:
                option = CreateRecordOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 3 之間的數字:")
        return option

    @classmethod
    def execute(cls, option):
        if option is CreateRecordOption.INCOME:
            cls.IE = FixedIEType.INCOME.name
        else :
            cls.IE = FixedIEType.EXPENSE.name
        cls.createRecord()

    @classmethod
    def createRecord(cls):
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

        cls.hintGetAmount()
        while True:
            try:
                amount = float(input())
                break
            except ValueError:
                cls.hintIntegerErorMsg()

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

        cls.hintGetConsumptionDate()
        while True:
            try:
                spendingTime = input()
                if (spendingTime == ""):
                    spendingTime = datetime.today().date()
                    break
                datetime.strptime(spendingTime, '%Y-%m-%d').date()
                break
            except ValueError:
                cls.hintGetConsumptionDate()

        if payment['category'] == PaymentCategory.CREDIT_CARD.name:
            cls.hintGetDeductionDate()
            while True:
                try:
                    deducteTime = input()
                    if (deducteTime == ""):
                        deducteTime = datetime.today().date()
                        break
                    datetime.strptime(deducteTime, '%Y-%m-%d').date()
                    break
                except ValueError:
                    cls.hintGetDeductionDate()
        else: deducteTime = spendingTime

        cls.hintGetNote()
        note = input()

        cls.hintGetInvoice()
        invoiceNumber = input()
        while invoiceNumber != "":
            try:
                pattern = r'\d{8}$'
                match = re.match(pattern, invoiceNumber)
                if match:
                    break
                else:
                    raise ValueError()
            except ValueError:
                cls.hintGetInvoice()
                invoiceNumber = input()

        cls.setUp_connection_and_table()
        query = cls.table.insert().values(IE=cls.IE,
                                          category=category,
                                          amount=amount, payment=payment['name'],
                                          location=location, consumptionDate=spendingTime,
                                          deductionDate=deducteTime, invoice=invoiceNumber, note=note)
        resultProxy = cls.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("新增資料失敗")
            cls.tearDown_connection(es.ROLLBACK)
            return
        cls.tearDown_connection(es.COMMIT)
        
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
    def hintGetConsumptionDate():
        print("請輸入消費日期(yyyy-mm-dd):")

    @staticmethod
    def hintGetDeductionDate():
        print("請輸入扣款日期(yyyy-mm-dd):")

    @staticmethod
    def hintIntegerErorMsg():
        print("請輸入數字:")

    @staticmethod
    def hintGetNote():
        print("請輸入備註:")

    @staticmethod
    def hintGetInvoice():
        print("請輸入發票末八碼數字:")

    @classmethod
    def start(cls):
        while True:
            cls.show()
            option = cls.choose()
            if option is CreateRecordOption.BACK:
                return
            cls.execute(option)

if __name__ == '__main__':  # pragma: no cover
    createRecordPage = CreateRecordPage()
    createRecordPage.start()