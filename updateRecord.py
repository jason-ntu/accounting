from enum import IntEnum, auto
from datetime import datetime
import sqlalchemy as sql
from accessor import Accessor, ExecutionStatus as es
from sqlalchemy import and_
from readRecord import ReadRecordPage, ReadRecordOption
from createRecord import PaymentOption, CreateRecordPage
import sys

class CategoryOption(IntEnum):
    CATEGORY = auto()
    PAYMENT = auto()
    AMOUNT = auto()
    PLACE = auto()
    TIME = auto()

class UpdateRecordPage(Accessor):

    table_name = "Record"
    IDerrorMsg = "輸入的ID須為整數"
    errorMsg = "請輸入 1 到 5 之間的數字: "
    categoryList = ["FOOD", "BEVERAGE"]
    paymentList = ["CASH", "DEBIT_CARD", "CREDIT_CARD", "ELECTRONIC", "OTHER"]

    def hintChooseCategory(self):
        print("請輸入要更改的項目")
        print("1 類別 2 支付方式 3 金額 4 地點 5 時間")
    
    def hintNewAmount(self):
        print("請輸入新的金額")
    
    def hintNewCategory(self):
        print("請選擇新的分類 1 食物 2 飲料")

    def hintNewPayment(self):
        print("請選擇新的支付方式 1 現金 2 借記卡 3 信用卡 4 電子支付 5 其他")
    
    def hintNewPlace(self):
        print("請輸入新的地點")
    
    def hintNewTime(self):
        print("請輸入新的日期(yyyy-mm-dd)")
    
    def chooseCategory(self):
        while True:
            try:
                self.hintChooseCategory()
                option = CategoryOption(int(input()))
                break
            except ValueError:
                print(self.errorMsg)
        return option
    
    def checkIDInteger(self):
        while True:
            try:
                ID = int(input("請輸入想更改的紀錄ID: "))
                break
            except ValueError:
                print(self.IDerrorMsg)
        return ID
    
    def updateCategory(self, ID):
        self.hintNewCategory()
        newCategory = int(input())
        self.setUp_connection_and_table()
        query = sql.update(self.table).where(self.table.c.id == ID).values(category=self.categoryList[newCategory-1])
        resultProxy = self.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            self.tearDown_connection(es.ROLLBACK)
            return
        self.tearDown_connection(es.COMMIT)


    def updatePayment(self, ID):
        self.hintNewPayment()
        newPayment = int(input())
        self.setUp_connection_and_table()
        query = sql.update(self.table).where(self.table.c.id == ID).values(payment=self.paymentList[newPayment-1])
        resultProxy = self.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            self.tearDown_connection(es.ROLLBACK)
            return
        self.tearDown_connection(es.COMMIT)

    def updateAmount(self, ID):
        self.hintNewAmount()
        newAmount = int(input())
        self.setUp_connection_and_table()
        query = sql.update(self.table).where(self.table.c.id == ID).values(amount=newAmount)
        resultProxy = self.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            self.tearDown_connection(es.ROLLBACK)
            return
        self.tearDown_connection(es.COMMIT)

    def updatePlace(self, ID):
        self.hintNewPlace()
        # newPlace = input().encode("utf-8")
        newPlace = input()
        self.setUp_connection_and_table()
        query = sql.update(self.table).where(self.table.c.id == ID).values(place=newPlace)
        resultProxy = self.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            self.tearDown_connection(es.ROLLBACK)
            return
        self.tearDown_connection(es.COMMIT)

    def updateTime(self, ID):
        self.hintNewTime()
        newTime = input()
        self.setUp_connection_and_table()
        query = sql.update(self.table).where(self.table.c.id == ID).values(time=newTime)
        resultProxy = self.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            self.tearDown_connection(es.ROLLBACK)
            return
        self.tearDown_connection(es.COMMIT)

    def updateDB(self, ID, option):
        if option is CategoryOption.CATEGORY:
            self.updateCategory(ID)
        elif option is CategoryOption.PAYMENT:
            self.updatePayment(ID)
        elif option is CategoryOption.AMOUNT:
            self.updateAmount(ID)
        elif option is CategoryOption.PLACE:
            self.updatePlace(ID)
        elif option is CategoryOption.TIME:
            self.updateTime(ID)
        else:
            raise ValueError(self.errorMsg)

    def updateByID(self):  # pragma: no cover
        ID = self.checkIDInteger()
        option = self.chooseCategory()
        self.updateDB(ID, option)

    def start(self):
        while True:
            readRecordPage = ReadRecordPage()
            readRecordPage.show()
            option = readRecordPage.choose()
            if option is ReadRecordOption.BACK:
                return
            readRecordPage.execute(option)
            self.updateByID()

if __name__ == '__main__':  # pragma: no cover
    updateRecordPage = UpdateRecordPage()
    updateRecordPage.start()