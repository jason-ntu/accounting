from enum import IntEnum, auto
from datetime import datetime
import sqlalchemy as sql
from accessor import Accessor, ExecutionStatus as es
from sqlalchemy import and_
from readRecord import ReadRecordPage, ReadRecordOption
from createRecord import PaymentOption, CreateRecordPage
import re

class ItemOption(IntEnum):
    IE = auto()
    CATEGORY = auto()
    PAYMENT = auto()
    AMOUNT = auto()
    PLACE = auto()
    CONSUMPTIONTIME = auto()
    DEDUCTIONTIME = auto()
    INVOICE = auto()
    NOTE = auto()

class UpdateRecordPage(Accessor):

    table_name = "Record"
    IDerrorMsg = "輸入的ID須為整數"
    errorMsg = "請輸入 1 到 9 之間的數字: "
    categoryList = ["FOOD", "BEVERAGE"]
    paymentList = ["CASH", "DEBIT_CARD", "CREDIT_CARD", "ELECTRONIC", "OTHER"]
    IEList = ["INCOME", "EXPENSE"]

    @staticmethod
    def hintChooseItem():
        print("請輸入要更改的項目")
        print("1 收入支出 2 類別 3 支付方式 4 金額 5 地點 6 消費時間 7 扣款時間 8 發票號碼 9 備註")

    @staticmethod
    def hintNewIE():
        print("請選擇 1 收入 2 支出")

    @staticmethod
    def hintNewAmount():
        print("請輸入新的金額")
    
    @staticmethod
    def hintNewCategory():
        print("請選擇新的分類 1 食物 2 飲料")

    @staticmethod
    def hintNewPayment():
        print("請選擇新的支付方式 1 現金 2 借記卡 3 信用卡 4 電子支付 5 其他")
    
    @staticmethod
    def hintNewPlace():
        print("請輸入新的地點")
    
    @staticmethod
    def hintNewTime():
        print("請輸入新的日期(yyyy-mm-dd)")
    
    @staticmethod
    def hintNewInvoice():
        print("請輸入新的發票號碼(發票末8碼數字)")
    
    @staticmethod
    def hintNewNote():
        print("請輸入新的備註")
    
    @staticmethod
    def hintIntegerErorMsg():
        print("輸入的數字須為整數")
    
    @classmethod
    def chooseItem(clf):
        while True:
            try:
                clf.hintChooseItem()
                option = ItemOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 9 之間的數字: ")
        return option
    
    @classmethod
    def checkIDInteger(clf):
        while True:
            try:
                ID = int(input("請輸入想更改的紀錄ID: "))
                break
            except ValueError:
                print("輸入的ID須為整數")
        return ID
    
    @classmethod
    def updateCategory(clf, ID):
        clf.hintNewCategory()
        while True:
            try:
                newCategory = int(input())
                if newCategory <= len(clf.categoryList):
                    break
                else: 
                    raise ValueError()
            except ValueError:
                clf.hintNewCategory()
        clf.setUp_connection_and_table()
        query = sql.update(clf.table).where(clf.table.c.id == ID).values(category=clf.categoryList[newCategory-1])
        resultProxy = clf.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            clf.tearDown_connection(es.ROLLBACK)
            return
        clf.tearDown_connection(es.COMMIT)

    @classmethod
    def updatePayment(clf, ID):
        clf.hintNewPayment()
        while True:
            try:
                newPayment = int(input())
                if newPayment <= len(clf.paymentList):
                    break
                else: 
                    raise ValueError()
            except ValueError:
                clf.hintNewPayment()

        clf.setUp_connection_and_table()
        query = sql.update(clf.table).where(clf.table.c.id == ID).values(payment=clf.paymentList[newPayment-1])
        resultProxy = clf.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            clf.tearDown_connection(es.ROLLBACK)
            return
        clf.tearDown_connection(es.COMMIT)

    @classmethod
    def updateAmount(clf, ID):
        clf.hintNewAmount()
        while True:
            try:
                newAmount = int(input())
                break
            except ValueError:
                clf.hintIntegerErorMsg()
        clf.setUp_connection_and_table()
        query = sql.update(clf.table).where(clf.table.c.id == ID).values(amount=newAmount)
        resultProxy = clf.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            clf.tearDown_connection(es.ROLLBACK)
            return
        clf.tearDown_connection(es.COMMIT)

    @classmethod
    def updatePlace(clf, ID):
        clf.hintNewPlace()
        newPlace = input()
        clf.setUp_connection_and_table()
        query = sql.update(clf.table).where(clf.table.c.id == ID).values(place=newPlace)
        resultProxy = clf.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            clf.tearDown_connection(es.ROLLBACK)
            return
        clf.tearDown_connection(es.COMMIT)
    
    @classmethod
    def updateIE(clf, ID):
        clf.hintNewIE()
        while True:
            try:
                newIE = int(input())
                if newIE <= len(clf.IEList):
                    break
                else: 
                    raise ValueError()
            except ValueError:
                clf.hintNewIE()
        clf.setUp_connection_and_table()
        query = sql.update(clf.table).where(clf.table.c.id == ID).values(IE=clf.IEList[newIE-1])
        resultProxy = clf.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            clf.tearDown_connection(es.ROLLBACK)
            return
        clf.tearDown_connection(es.COMMIT)

    @classmethod
    def updateConsumptionDate(clf, ID):
        clf.hintNewTime()
        while True:
            try:
                newTime = input()
                datetime.strptime(newTime, '%Y-%m-%d').date()
                break
            except ValueError:
                clf.hintNewTime()

        clf.setUp_connection_and_table()
        query = sql.update(clf.table).where(clf.table.c.id == ID).values(consumptionDate=newTime)
        resultProxy = clf.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            clf.tearDown_connection(es.ROLLBACK)
            return
        clf.tearDown_connection(es.COMMIT)

    @classmethod
    def updateDeductionDate(clf, ID):
        clf.hintNewTime()
        while True:
            try:
                newTime = input()
                datetime.strptime(newTime, '%Y-%m-%d').date()
                break
            except ValueError:
                clf.hintNewTime()
        clf.setUp_connection_and_table()
        query = sql.update(clf.table).where(clf.table.c.id == ID).values(deductionDate=newTime)
        resultProxy = clf.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            clf.tearDown_connection(es.ROLLBACK)
            return
        clf.tearDown_connection(es.COMMIT)

    @classmethod
    def updateInvoice(clf, ID):
        clf.hintNewInvoice()
        newInvoice = input()
        while newInvoice != "":
            try:
                pattern = r'\d{8}$'
                match = re.match(pattern, newInvoice)
                if match:
                    break
                else:
                    raise ValueError()
            except ValueError:
                clf.hintNewInvoice()
                newInvoice = input()
        clf.setUp_connection_and_table()
        query = sql.update(clf.table).where(clf.table.c.id == ID).values(invoice=newInvoice)
        resultProxy = clf.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            clf.tearDown_connection(es.ROLLBACK)
            return
        clf.tearDown_connection(es.COMMIT)

    @classmethod
    def updateNote(clf, ID):
        clf.hintNewNote()
        newNote = input()
        clf.setUp_connection_and_table()
        query = sql.update(clf.table).where(clf.table.c.id == ID).values(note=newNote)
        resultProxy = clf.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            clf.tearDown_connection(es.ROLLBACK)
            return
        clf.tearDown_connection(es.COMMIT)

    @classmethod
    def updateDB(clf, ID, option):
        if option is ItemOption.IE:
            clf.updateIE(ID)
        elif option is ItemOption.CATEGORY:
            clf.updateCategory(ID)
        elif option is ItemOption.PAYMENT:
            clf.updatePayment(ID)
        elif option is ItemOption.AMOUNT:
            clf.updateAmount(ID)
        elif option is ItemOption.PLACE:
            clf.updatePlace(ID)
        elif option is ItemOption.CONSUMPTIONTIME:
            clf.updateConsumptionDate(ID)
        elif option is ItemOption.DEDUCTIONTIME:
            clf.updateDeductionDate(ID)
        elif option is ItemOption.INVOICE:
            clf.updateInvoice(ID)
        elif option is ItemOption.NOTE:
            clf.updateNote(ID)
        else:
            raise ValueError(clf.errorMsg)

    @classmethod
    def updateByID(clf):  # pragma: no cover
        ID = clf.checkIDInteger()
        option = clf.chooseItem()
        clf.updateDB(ID, option)

    @classmethod
    def start(clf):
        while True:
            readRecordPage = ReadRecordPage()
            readRecordPage.show()
            option = readRecordPage.choose()
            if option is ReadRecordOption.BACK:
                return
            readRecordPage.execute(option)
            clf.updateByID()

if __name__ == '__main__':  # pragma: no cover
    updateRecordPage = UpdateRecordPage()
    updateRecordPage.start()