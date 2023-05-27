from enum import IntEnum, auto
from accessor import ExecutionStatus as es
import sys
from account import AccountCategory
from records import RecordPage
from IEDirection import IEDirection

class CreateRecordOption(IntEnum):
    INCOME = IEDirection.INCOME
    EXPENSE = IEDirection.EXPENSE
    BACK = auto()

class CreateRecordPage(RecordPage):

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
        if option is IEDirection.INCOME:
            cls.IE = IEDirection.INCOME.name
        else :
            cls.IE = IEDirection.EXPENSE.name
        cls.createRecord()

    @classmethod
    def createRecord(cls):
        category = cls.askCategory()
        account = cls.askAccount()
        amount = cls.askAmount()
        location = cls.askLocation()
        purchaseDate = cls.askPurchaseDate()
        debitDate = purchaseDate
        if account['category'] == AccountCategory.CREDIT_CARD.name:
            debitDate = cls.askDebitDate()
        invoice = cls.askInvoice()
        note = cls.askNote()

        cls.setUp_connection_and_table()
        query = cls.table.insert().values(IE=cls.IE,category=category,
                                          amount=amount, account=account['name'],
                                          location=location, purchaseDate=purchaseDate,
                                          debitDate=debitDate, invoice=invoice, note=note)
        resultProxy = cls.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("新增資料失敗")
            cls.tearDown_connection(es.ROLLBACK)
            return
        cls.tearDown_connection(es.COMMIT)
        cls.updateAccountAmount(cls.IE, account['name'], amount)

    @classmethod
    def start(cls):
        while True:
            cls.show()
            option = cls.choose()
            if option is CreateRecordOption.BACK:
                return
            cls.execute(option)

if __name__ == '__main__':  # pragma: no cover
    CreateRecordPage.start()