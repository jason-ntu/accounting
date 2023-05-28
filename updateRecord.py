from enum import IntEnum, auto
import sqlalchemy as sql
from accessor import ExecutionStatus as es
from readRecord import ReadRecordPage, ReadRecordOption
from records import RecordPage
from account import AccountPage

class ItemOption(IntEnum):
    IE = auto()
    CATEGORY = auto()
    ACCOUNT = auto()
    AMOUNT = auto()
    LOCATION = auto()
    CONSUMPTIONTIME = auto()
    DEDUCTIONTIME = auto()
    INVOICE = auto()
    NOTE = auto()

class UpdateRecordPage(RecordPage):

    @staticmethod
    def hintChooseItem():
        print("1 收入支出 2 類別 3 帳戶 4 金額 5 地點 6 消費時間 7 扣款時間 8 發票號碼 9 備註")
        print("請輸入要更改的項目:")

    @staticmethod
    def hintGetCategory():
        print("請輸入新的紀錄類型:")

    @staticmethod
    def hintGetAccount():
        print("請輸入新的帳戶:")

    @staticmethod
    def hintGetAmount():
        print("請輸入新的金額:")

    @staticmethod
    def hintGetLocation():
        print("請輸入新的消費地點:")
    
    @staticmethod
    def hintGetPurchaseDate():
        print("請輸入新的消費日期(yyyy-mm-dd):")
    
    @staticmethod
    def hintGetDebitDate():
        print("請輸入新的扣款日期(yyyy-mm-dd):")
    
    @staticmethod
    def hintGetInvoice():
        print("請輸入新的發票號碼(發票末8碼數字):")
    
    @staticmethod
    def hintGetNote():
        print("請輸入新的備註:")
    
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
        cls.setUp_connection_and_table()
        query = sql.select(cls.table.c['IE']).where(cls.table.c.id == ID)
        results = cls.conn.execute(query).first()
        if results is None:
            successful = False
        else:
            cls.IE = results[0]
            newCategory = cls.askCategory()
            query = sql.update(cls.table).where(cls.table.c.id == ID).values(category=newCategory)
            resultProxy = cls.conn.execute(query)
            successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            cls.tearDown_connection(es.ROLLBACK)
            return
        cls.tearDown_connection(es.COMMIT)

    @classmethod
    def updateAccount(cls, ID):
        newAccount = cls.askAccount()
        cls.setUp_connection_and_table()
        query = sql.update(cls.table).where(cls.table.c.id == ID).values(account=newAccount['name'])
        resultProxy = cls.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            cls.tearDown_connection(es.ROLLBACK)
            return
        cls.tearDown_connection(es.COMMIT)

    @classmethod
    def updateAmount(cls, ID):
        newAmount = cls.askAmount()
        cls.setUp_connection_and_table([cls.table_name, AccountPage.table_name])

        query = sql.select(cls.tables[0]).where(cls.tables[0].c.id == ID)
        results = cls.conn.execute(query).fetchall()
        dictRow = results[0]._asdict() 
        originIE = dictRow['IE']
        originAccount = dictRow['account']
        originAmount = dictRow['amount']    
            
        query = sql.update(cls.tables[0]).where(cls.tables[0].c.id == ID).values(amount=newAmount)
        resultProxy = cls.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            cls.tearDown_connection(es.ROLLBACK)
            return
        cls.updateAccountAmount(originIE, originAccount, newAmount-originAmount)

    @classmethod
    def updateLocation(cls, ID):
        newLocation = cls.askLocation()
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
        newIE = cls.askIE()
        cls.setUp_connection_and_table()
        query = sql.update(cls.table).where(cls.table.c.id == ID).values(IE=newIE.name)
        resultProxy = cls.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            cls.tearDown_connection(es.ROLLBACK)
            return
        cls.tearDown_connection(es.COMMIT)

    @classmethod
    def updatePurchaseDate(cls, ID):
        newDate = cls.askPurchaseDate()
        cls.setUp_connection_and_table()
        query = sql.update(cls.table).where(cls.table.c.id == ID).values(purchaseDate=newDate)
        resultProxy = cls.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            cls.tearDown_connection(es.ROLLBACK)
            return
        cls.tearDown_connection(es.COMMIT)

    @classmethod
    def updateDebitDate(cls, ID):
        newDate = cls.askDebitDate()
        cls.setUp_connection_and_table()
        query = sql.update(cls.table).where(cls.table.c.id == ID).values(debitDate=newDate)
        resultProxy = cls.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            cls.tearDown_connection(es.ROLLBACK)
            return
        cls.tearDown_connection(es.COMMIT)

    @classmethod
    def updateInvoice(cls, ID):
        newInvoice = cls.askInvoice()
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
    def updateNote(cls, ID):
        newNote = cls.askNote()
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
        elif option is ItemOption.ACCOUNT:
            cls.updateAccount(ID)
        elif option is ItemOption.AMOUNT:
            cls.updateAmount(ID)
        elif option is ItemOption.LOCATION:
            cls.updateLocation(ID)
        elif option is ItemOption.CONSUMPTIONTIME:
            cls.updatePurchaseDate(ID)
        elif option is ItemOption.DEDUCTIONTIME:
            cls.updateDebitDate(ID)
        elif option is ItemOption.INVOICE:
            cls.updateInvoice(ID)
        else: 
            cls.updateNote(ID)
        
    @classmethod
    def updateByID(cls):  
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
    UpdateRecordPage.start()