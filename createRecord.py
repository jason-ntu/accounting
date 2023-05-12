from enum import IntEnum, auto
from accessor import Accessor
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
    BACK = auto()

class CreateRecordPage(Accessor):

    errorMsg = "請輸入 1 到 3 之間的數字:"
    paymentErrorMsg = "請輸入 1 到 5 之間的數字:"
    category = ""
    table_name = "Record"
    paymentMsg = "支付方式 1 現金 2 借記卡 3 信用卡 4 電子支付 5 其他: "
    IntegerErrorMsg = "輸入的數字須為整數"
    
    
    def show(self):
        print("%d: 新增食物類別" % CreateRecordOption.FOOD)
        print("%d: 新增飲料類別" % CreateRecordOption.BEVERAGE)
        print("%d: 回到上一頁" % CreateRecordOption.BACK)

    def choose(self):
        while True:
            try:
                option = CreateRecordOption(int(input()))
                break
            except ValueError:
                print(self.errorMsg)
        return option

    def choosePayment(self):
        while True:
            try:
                option = PaymentOption(int(input(self.paymentMsg)))
                break
            except ValueError:
                print(self.paymentErrorMsg)
        return option.name

    def execute(self, option):
        if option is CreateRecordOption.FOOD:
            self.category = "FOOD"
        elif option is CreateRecordOption.BEVERAGE:
            self.category = "BEVERAGE"
        else:
            raise ValueError(self.errorMsg)
        
        self.createRecord()
    
    def createRecord(self):
        payment = self.choosePayment()
        self.hintGetAmount()
        amountOfMoney = self.getAmount()
        self.hintGetPlace()
        consumptionPlace = input()
        self.hintGetTime()
        spendingTime = str(input())
        if (spendingTime == ""):
            spendingTime = datetime.today().date()
        self.setUp_connection_and_table()
        query = self.table.insert().values(category=self.category, amount=amountOfMoney, payment=payment, place=consumptionPlace, time=spendingTime)
        rowsAffected = self.conn.execute(query).rowcount
        self.tearDown_connection()
        # return rowsAffected == 1
    
    def getAmount(self):
        while True:
            try:
                money = int(input())
                break
            except ValueError:
                print(self.IntegerErrorMsg)
        return money
    
    def hintGetAmount(self):
        print("請輸入金額")
    
    def hintGetPlace(self):
        print("請輸入消費地點")
    
    def hintGetTime(self):
        print("請輸入消費時間(yyyy-mm-dd)")

    def start(self):
        while True:
            self.show()
            option = self.choose()
            if option is CreateRecordOption.BACK:
                return
            self.execute(option)

if __name__ == '__main__':  # pragma: no cover
    createRecordPage = CreateRecordPage()
    createRecordPage.start()
