from enum import IntEnum, auto
from datetime import datetime
import sqlalchemy as sql
from accessor import Accessor, ExecutionStatus as es
from readRecord import ReadRecordPage, ReadRecordOption

class DeleteRecordPage(Accessor):

    table_name = "Record"

    @staticmethod
    def hintGetID():
        print("請輸入想刪除的紀錄ID: ")
            
    @classmethod
    def checkIDInteger(clf):
        while True:
            try:
                clf.hintGetID()
                ID = int(input())
                break
            except ValueError:
                print("輸入的ID須為整數")
        return ID

    @classmethod
    def deleteByID(clf):
        ID = clf.checkIDInteger()
        clf.setUp_connection_and_table()
        query = sql.delete(clf.table).where(clf.table.c.id == ID)
        resultProxy = clf.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("此紀錄ID不存在")
            clf.tearDown_connection(es.ROLLBACK)
            return
        clf.tearDown_connection(es.COMMIT)

    @classmethod
    def start(clf):
        while True:
            readRecordPage = ReadRecordPage()
            readRecordPage.show()
            option = readRecordPage.choose()
            if option is ReadRecordOption.BACK:
                return
            readRecordPage.execute(option)
            clf.deleteByID()

if __name__ == '__main__':  # pragma: no cover
    deleteRecordPage = DeleteRecordPage()
    deleteRecordPage.start()