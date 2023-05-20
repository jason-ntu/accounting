from enum import IntEnum, auto
from accessor import Accessor, ExecutionStatus as es
import sqlalchemy as sql
import sys
from datetime import datetime
import re
from fixedIE import FixedIEType
from category import CategoryPage


class CreateRecordOption(IntEnum):
    INCOME = auto()
    EXPENSE = auto()
    BACK = auto()

class PaymentOption(IntEnum):
    CASH = auto()
    DEBIT_CARD = auto()
    CREDIT_CARD = auto()
    ELECTRONIC = auto()
    OTHER = auto()

class CreateRecordPage(Accessor):

    IE = ""
    categoryList = []
    table_name = "Record"

    @staticmethod
    def show():
        print("%d: 新增收入" % CreateRecordOption.INCOME)
        print("%d: 新增支出" % CreateRecordOption.EXPENSE)
        print("%d: 回到上一頁" % CreateRecordOption.BACK)

    @classmethod
    def showCategory(clf):
        for i in range(len(clf.categoryList)):
            print("%d %s" % (i+1, clf.categoryList[i]))

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
    def execute(clf, option):
        if option is CreateRecordOption.INCOME:
            clf.IE = FixedIEType.INCOME.name
        else :
            clf.IE = FixedIEType.EXPENSE.name
        clf.createRecord()

    @classmethod
    def createRecord(clf):
        clf.categoryList = CategoryPage.getList()
        while True:
            clf.showCategory()
            clf.hintGetCategory()
            try:
                choice = int(input())
                if choice not in range(1, len(clf.categoryList)+1):
                    raise ValueError
                categoryOption = clf.categoryList[choice-1]
                break
            except ValueError:
                print("請輸入 1 到 %d 之間的數字:" % len(clf.categoryList))

        while True:
            clf.hintPaymentMsg()
            try:
                paymentOption = PaymentOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 5 之間的數字:")

        clf.hintGetAmount()
        while True:
            try:
                amountOfMoney = int(input())
                break
            except ValueError:
                clf.hintIntegerErorMsg()

        clf.hintGetPlace()
        consumptionPlace = input()
        clf.hintGetConsumptionDate()
        while True:
            try:
                spendingTime = input()
                datetime.strptime(spendingTime, '%Y-%m-%d').date()
                break
            except ValueError:
                clf.hintGetConsumptionDate()

        if paymentOption is paymentOption.CREDIT_CARD:
            clf.hintGetDeductionDate()
            while True:
                try:
                    deducteTime = input()
                    datetime.strptime(deducteTime, '%Y-%m-%d').date()
                    break
                except ValueError:
                    clf.hintGetDeductionDate()
        else: deducteTime = spendingTime

        clf.hintGetNote()
        note = input()

        clf.hintGetInvoice()
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
                clf.hintGetInvoice()
                invoiceNumber = input()

        clf.setUp_connection_and_table()
        query = clf.table.insert().values(IE=clf.IE,
                                        #   TODO: update this
                                          category=categoryOption,
                                          amount=amountOfMoney, payment=paymentOption.name,
                                          place=consumptionPlace, consumptionDate=spendingTime,
                                          deductionDate=deducteTime, invoice=invoiceNumber, note=note)
        resultProxy = clf.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("新增資料失敗")
            clf.tearDown_connection(es.ROLLBACK)
            return
        clf.tearDown_connection(es.COMMIT)

    @staticmethod
    def hintGetCategory():
        print("請選擇紀錄類別")

    @staticmethod
    def hintPaymentMsg():
        print("收支方式 1 現金 2 借記卡 3 信用卡 4 電子支付 5 其他: ")

    @staticmethod
    def hintGetAmount():
        print("請輸入金額")

    @staticmethod
    def hintGetPlace():
        print("請輸入消費地點")

    @staticmethod
    def hintGetConsumptionDate():
        print("請輸入消費日期(yyyy-mm-dd)")

    @staticmethod
    def hintGetDeductionDate():
        print("請輸入扣款日期(yyyy-mm-dd)")

    @staticmethod
    def hintIntegerErorMsg():
        print("輸入的數字須為整數")

    @staticmethod
    def hintGetNote():
        print("請輸入備註")

    @staticmethod
    def hintGetInvoice():
        print("請輸入發票末八碼數字")

    @classmethod
    def start(clf):
        while True:
            clf.show()
            option = clf.choose()
            if option is CreateRecordOption.BACK:
                return
            clf.execute(option)

if __name__ == '__main__':  # pragma: no cover
    createRecordPage = CreateRecordPage()
    createRecordPage.start()