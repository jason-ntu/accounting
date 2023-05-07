from enum import IntEnum, auto
from accessor import Accessor
import sqlalchemy as sql
import sys

class AddRecordOption(IntEnum):
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


class AddRecordPage(Accessor):

    errorMsg = "請輸入 1 到 3 之間的數字:"
    paymentErrorMsg = "請輸入 1 到 6 之間的數字:"
    category = ""
    table_name = "Record"
    
    def show(self):
        print("%d: 新增食物類別" % AddRecordOption.FOOD)
        print("%d: 新增飲料類別" % AddRecordOption.BEVERAGE)
        print("%d: 回到上一頁" % AddRecordOption.BACK)

    def choose(self):
        while True:
            try:
                option = AddRecordOption(int(input()))
                break
            except ValueError:
                print(self.errorMsg)
        return option

    def choosePayment(self):
        msg = "類型(1 現金, 2 借記卡, 3 信用卡, 4 電子支付, 5 其他, 6 回到上一頁): "
        while True:
            try:
                option = PaymentOption(int(input(msg)))
                break
            except ValueError:
                print(self.paymentErrorMsg)
        return option.name

    def execute(self, option):
        if option is AddRecordOption.FOOD:
            self.category = "FOOD"
        elif option is AddRecordOption.BEVERAGE:
            self.category = "BEVERAGE"
        else:
            raise ValueError(self.errorMsg)
        
        self.createRecord()
    
    def createRecord(self):
        payment = self.choosePayment()
        # if payment is PaymentOption.BACK:
        #     return
        amountOfMoney = int(input("請輸入金額: "))
        consumptionPlace = str(input("請輸入消費地點: "))
        spendingTime = str(input("請輸入消費時間(yyyy-mm-dd): "))
        self.setUp_connection_and_table()
        query = self.table.insert().values(category=self.category, amount=amountOfMoney, payment=payment, place=consumptionPlace, time=spendingTime)
        rowsAffected = self.conn.execute(query).rowcount
        self.tearDown_connection()
        # return rowsAffected == 1

    def start(self):
        while True:
            self.show()
            option = self.choose()
            if option is AddRecordOption.BACK:
                return
            self.execute(option)

if __name__ == '__main__':  # pragma: no cover
    addRecordPage = AddRecordPage()
    addRecordPage.start()
