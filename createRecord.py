from enum import IntEnum, auto
from accessor import Accessor, ExecutionStatus as es
import sqlalchemy as sql
import sys
from datetime import datetime


class CreateRecordOption(IntEnum):
    FOOD = auto()
    BEVERAGE = auto()
    BACK = auto()

class PaymentOption(IntEnum):
    CASH = auto()
    DEBIT_CARD = auto()
    CREDIT_CARD = auto()
    ELECTRONIC = auto()
    OTHER = auto()

class CreateRecordPage(Accessor):

    errorMsg = "請輸入 1 到 3 之間的數字:"
    category = ""
    table_name = "Record"
    
    @staticmethod
    def show():
        print("%d: 新增食物類別" % CreateRecordOption.FOOD)
        print("%d: 新增飲料類別" % CreateRecordOption.BEVERAGE)
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

    @staticmethod
    def choosePayment():
        while True:
            print("支付方式 1 現金 2 借記卡 3 信用卡 4 電子支付 5 其他: ")
            try:
                option = PaymentOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 5 之間的數字:")
        return option.name
        
    @classmethod
    def execute(clf, option):
        if option is CreateRecordOption.FOOD:
            clf.category = "FOOD"
        elif option is CreateRecordOption.BEVERAGE:
            clf.category = "BEVERAGE"
        else:
            raise ValueError(clf.errorMsg)
        clf.createRecord()
    
    @classmethod
    def createRecord(clf):
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
        clf.hintGetTime()
        while True:
            try:
                spendingTime = input()
                datetime.strptime(spendingTime, '%Y-%m-%d').date()
                break
            except ValueError:
                clf.hintGetTime()
        if (spendingTime == ""):
            spendingTime = datetime.today().date()
        clf.setUp_connection_and_table()
        query = clf.table.insert().values(category=clf.category, amount=amountOfMoney, payment=paymentOption.name, place=consumptionPlace, time=spendingTime)
        resultProxy = clf.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("新增資料失敗")
            clf.tearDown_connection(es.ROLLBACK)
            return
        clf.tearDown_connection(es.COMMIT)
    
    @staticmethod
    def hintGetAmount():
        print("請輸入金額")
    
    @staticmethod
    def hintGetPlace():
        print("請輸入消費地點")

    @staticmethod
    def hintGetTime():
        print("請輸入消費時間(yyyy-mm-dd)")

    @staticmethod
    def hintIntegerErorMsg():
        print("輸入的數字須為整數")

    @staticmethod
    def hintPaymentMsg():
        print("支付方式 1 現金 2 借記卡 3 信用卡 4 電子支付 5 其他: ")

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
