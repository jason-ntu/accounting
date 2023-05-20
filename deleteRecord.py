from enum import IntEnum, auto
from datetime import datetime
import sqlalchemy as sql
from accessor import Accessor, ExecutionStatus as es
from readRecord import ReadRecordPage, ReadRecordOption

class DeleteRecordPage(Accessor):

    errorMsg = "請輸入 1 到 3 之間的數字:"
    table_name = "Record"
    IDerrorMsg = "輸入的ID須為整數"

            
    def checkIDInteger(self):
        while True:
            try:
                ID = int(input("請輸入想刪除的紀錄ID: "))
                break
            except ValueError:
                print(self.IDerrorMsg)
        return ID

    def deleteByID(self):
        ID = self.checkIDInteger()
        self.setUp_connection_and_table()
        query = sql.delete(self.table).where(self.table.c.id == ID)
        resultProxy = self.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            self.tearDown_connection(es.ROLLBACK)
            return
        self.tearDown_connection(es.COMMIT)


    def start(self):
        while True:
            readRecordPage = ReadRecordPage()
            readRecordPage.show()
            option = readRecordPage.choose()
            if option is ReadRecordOption.BACK:
                return
            readRecordPage.execute(option)
            self.deleteByID()

if __name__ == '__main__':  # pragma: no cover
    deleteRecordPage = DeleteRecordPage()
    deleteRecordPage.start()