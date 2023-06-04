import sqlalchemy as sql
from accessor import ExecutionStatus as es
from readRecord import ReadRecordPage, ReadRecordOption
from records import RecordPage
from account import AccountPage

class DeleteRecordPage(RecordPage):

    @staticmethod
    def hintGetID():
        print("請輸入想刪除的紀錄ID:")

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
    def deleteByID(cls):
        ID = cls.checkIDInteger()
        cls.setUp_connection_and_table([cls.table_name, AccountPage.table_name])

        query = sql.select(cls.tables[0]).where(cls.tables[0].c.id == ID)
        results = cls.conn.execute(query).fetchone()
        if results is None:
            successful = False
        else:
            dictRow = results._asdict()
            originIE = dictRow['IE']
            originAccount = dictRow['account']
            originAmount = dictRow['amount']

            query = sql.delete(cls.tables[0]).where(cls.tables[0].c.id == ID)
            resultProxy = cls.conn.execute(query)
            successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            cls.tearDown_connection(es.ROLLBACK)
            return
        cls.updateAccountAmount(originIE, originAccount, -originAmount)

    @classmethod
    def start(cls):
        while True:
            readRecordPage = ReadRecordPage()
            readRecordPage.show()
            option = readRecordPage.choose()
            if option is ReadRecordOption.BACK:
                return
            readRecordPage.execute(option)
            cls.deleteByID()