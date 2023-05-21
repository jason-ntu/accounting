from enum import IntEnum, auto
from datetime import datetime
import sqlalchemy as sql
from accessor import ExecutionStatus as es
from sqlalchemy import and_
from readRecord import ReadRecordPage, ReadRecordOption
from records import RecordPage
from category import CategoryPage
from payment import PaymentPage
from location import LocationPage
import re

class ItemOption(IntEnum):
    IE = auto()
    CATEGORY = auto()
    PAYMENT = auto()
    AMOUNT = auto()
    LOCATION = auto()
    CONSUMPTIONTIME = auto()
    DEDUCTIONTIME = auto()
    INVOICE = auto()
    NOTE = auto()

class UpdateRecordPage(RecordPage):

    IEList = ["INCOME", "EXPENSE"]

    @staticmethod
    def hintChooseItem():
        print("1 收入支出 2 類別 3 收支方式 4 金額 5 地點 6 消費時間 7 扣款時間 8 發票號碼 9 備註")
        print("請輸入要更改的項目:")

    @staticmethod
    def hintGetIE():
        print("1 收入 2 支出")
        print("請選擇新的收入/支出:")

    @staticmethod
    def hintGetCategory():
        print("請輸入新的紀錄類型:")

    @staticmethod
    def hintGetPayment():
        print("請輸入新的收支方式:")

    @staticmethod
    def hintGetAmount():
        print("請輸入新的金額:")

    @staticmethod
    def hintGetLocation():
        print("請輸入新的消費地點:")
    
    @staticmethod
    def hintGetTime():
        print("請輸入新的日期(yyyy-mm-dd):")
    
    @staticmethod
    def hintGetInvoice():
        print("請輸入新的發票號碼(發票末8碼數字):")
    
    @staticmethod
    def hintGetNote():
        print("請輸入新的備註:")
    
    @staticmethod
    def hintIntegerErorMsg():
        print("輸入的數字須為整數:")
    
    @staticmethod
    def hintGetID():
        print("請輸入想更改的紀錄ID:")
    
    @classmethod
    def chooseItem(cls):
        while True:
            try:
                cls.hintChooseItem()
                option = ItemOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 9 之間的數字:")
        return option
    
    @classmethod
    def checkIDInteger(cls):
        while True:
            try:
                cls.hintGetID()
                ID = int(input())
                break
            except ValueError:
                print("輸入的ID須為整數")
        return ID
    
    @classmethod
    def updateCategory(cls, ID):
        newCategory = cls.askCategory()
        cls.setUp_connection_and_table()
        query = sql.update(cls.table).where(cls.table.c.id == ID).values(category=newCategory)
        resultProxy = cls.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            cls.tearDown_connection(es.ROLLBACK)
            return
        cls.tearDown_connection(es.COMMIT)

    @classmethod
    def updatePayment(cls, ID):
<<<<<<< HEAD
        cls.paymentList = PaymentPage.getList()
        cls.showPayment()
        cls.hintNewPayment()
        while True:
            try:
                choice  = int(input())
                if choice not in range(1, len(cls.paymentList)+1):
                    raise ValueError
                newPayment = cls.paymentList[choice-1]
                break
            except ValueError:
                cls.hintRetryPayment()
=======
        newPayment = cls.askPayment()
>>>>>>> 970ecc0 (payment)
        cls.setUp_connection_and_table()
        query = sql.update(cls.table).where(cls.table.c.id == ID).values(payment=newPayment['name'])
        resultProxy = cls.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            cls.tearDown_connection(es.ROLLBACK)
            return
        cls.tearDown_connection(es.COMMIT)

    @classmethod
<<<<<<< HEAD
    def updateAmount(cls, ID):
        cls.hintNewAmount()
=======
    def updateAmount(clf, ID):
        clf.hintGetAmount()
>>>>>>> 970ecc0 (payment)
        while True:
            try:
                newAmount = int(input())
                break
            except ValueError:
                cls.hintIntegerErorMsg()
        cls.setUp_connection_and_table()
        query = sql.update(cls.table).where(cls.table.c.id == ID).values(amount=newAmount)
        resultProxy = cls.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            cls.tearDown_connection(es.ROLLBACK)
            return
        cls.tearDown_connection(es.COMMIT)

    @classmethod
    def updateLocation(cls, ID):
        cls.locationList = LocationPage.getList()
        cls.showLocation()
        cls.hintNewLocation()
        while True:
            try:
                choice = int(input())
                if choice not in range(1, len(cls.locationList)+1):
                    raise ValueError
                newLocation = cls.locationList[choice-1]
                break
            except ValueError:
                cls.hintRetryLocation()
        cls.setUp_connection_and_table()
        query = sql.update(cls.table).where(cls.table.c.id == ID).values(location=newLocation)
        resultProxy = cls.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            cls.tearDown_connection(es.ROLLBACK)
            return
        cls.tearDown_connection(es.COMMIT)
    
    @classmethod
    def updateIE(cls, ID):
<<<<<<< HEAD
        cls.hintNewIE()
=======
        cls.hintGetIE()
>>>>>>> 970ecc0 (payment)
        while True:
            try:
                newIE = int(input())
                if newIE <= len(cls.IEList):
                    break
                else: 
                    raise ValueError()
            except ValueError:
<<<<<<< HEAD
                cls.hintNewIE()
=======
                cls.hintGetIE()
>>>>>>> 970ecc0 (payment)
        cls.setUp_connection_and_table()
        query = sql.update(cls.table).where(cls.table.c.id == ID).values(IE=cls.IEList[newIE-1])
        resultProxy = cls.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            cls.tearDown_connection(es.ROLLBACK)
            return
        cls.tearDown_connection(es.COMMIT)

    @classmethod
    def updateConsumptionDate(cls, ID):
<<<<<<< HEAD
        cls.hintNewTime()
=======
        cls.hintGetTime()
>>>>>>> 970ecc0 (payment)
        while True:
            try:
                newTime = input()
                datetime.strptime(newTime, '%Y-%m-%d').date()
                break
            except ValueError:
<<<<<<< HEAD
                cls.hintNewTime()
=======
                cls.hintGetTime()
>>>>>>> 970ecc0 (payment)

        cls.setUp_connection_and_table()
        query = sql.update(cls.table).where(cls.table.c.id == ID).values(consumptionDate=newTime)
        resultProxy = cls.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            cls.tearDown_connection(es.ROLLBACK)
            return
        cls.tearDown_connection(es.COMMIT)

    @classmethod
<<<<<<< HEAD
    def updateDeductionDate(cls, ID):
        cls.hintNewTime()
=======
    def updateDeductionDate(clf, ID):
        clf.hintGetTime()
>>>>>>> 970ecc0 (payment)
        while True:
            try:
                newTime = input()
                datetime.strptime(newTime, '%Y-%m-%d').date()
                break
            except ValueError:
<<<<<<< HEAD
                cls.hintNewTime()
        cls.setUp_connection_and_table()
        query = sql.update(cls.table).where(cls.table.c.id == ID).values(deductionDate=newTime)
        resultProxy = cls.conn.execute(query)
=======
                clf.hintGetTime()
        clf.setUp_connection_and_table()
        query = sql.update(clf.table).where(clf.table.c.id == ID).values(deductionDate=newTime)
        resultProxy = clf.conn.execute(query)
>>>>>>> 970ecc0 (payment)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            cls.tearDown_connection(es.ROLLBACK)
            return
        cls.tearDown_connection(es.COMMIT)

    @classmethod
<<<<<<< HEAD
    def updateInvoice(cls, ID):
        cls.hintNewInvoice()
=======
    def updateInvoice(clf, ID):
        clf.hintGetInvoice()
>>>>>>> 970ecc0 (payment)
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
<<<<<<< HEAD
                cls.hintNewInvoice()
=======
                clf.hintGetInvoice()
>>>>>>> 970ecc0 (payment)
                newInvoice = input()
        cls.setUp_connection_and_table()
        query = sql.update(cls.table).where(cls.table.c.id == ID).values(invoice=newInvoice)
        resultProxy = cls.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            cls.tearDown_connection(es.ROLLBACK)
            return
        cls.tearDown_connection(es.COMMIT)

    @classmethod
<<<<<<< HEAD
    def updateNote(cls, ID):
        cls.hintNewNote()
=======
    def updateNote(clf, ID):
        clf.hintGetNote()
>>>>>>> 970ecc0 (payment)
        newNote = input()
        cls.setUp_connection_and_table()
        query = sql.update(cls.table).where(cls.table.c.id == ID).values(note=newNote)
        resultProxy = cls.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            cls.tearDown_connection(es.ROLLBACK)
            return
        cls.tearDown_connection(es.COMMIT)

    @classmethod
    def updateDB(cls, ID, option):
        if option is ItemOption.IE:
            cls.updateIE(ID)
        elif option is ItemOption.CATEGORY:
            cls.updateCategory(ID)
        elif option is ItemOption.PAYMENT:
            cls.updatePayment(ID)
        elif option is ItemOption.AMOUNT:
            cls.updateAmount(ID)
        elif option is ItemOption.LOCATION:
            cls.updateLocation(ID)
        elif option is ItemOption.CONSUMPTIONTIME:
            cls.updateConsumptionDate(ID)
        elif option is ItemOption.DEDUCTIONTIME:
            cls.updateDeductionDate(ID)
        elif option is ItemOption.INVOICE:
            cls.updateInvoice(ID)
        else: 
            cls.updateNote(ID)
        

    @classmethod
    def updateByID(cls):  # pragma: no cover
        ID = cls.checkIDInteger()
        option = cls.chooseItem()
        cls.updateDB(ID, option)

    @classmethod
    def start(cls):
        while True:
            readRecordPage = ReadRecordPage()
            readRecordPage.show()
            option = readRecordPage.choose()
            if option is ReadRecordOption.BACK:
                return
            readRecordPage.execute(option)
            cls.updateByID()

if __name__ == '__main__':  # pragma: no cover
    updateRecordPage = UpdateRecordPage()
    updateRecordPage.start()