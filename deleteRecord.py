from enum import IntEnum, auto
from datetime import datetime
import sqlalchemy as sql
from accessor import Accessor


class DeleteRecordOption(IntEnum):
    ALL = auto()
    DATE = auto()
    BACK = auto()

class DeleteRecordPage(Accessor):

    errorMsg = "請輸入 1 到 3 之間的數字:"
    table_name = "Record"
    IDerrorMsg = "輸入的ID須為整數"

    def show(self):
        print("%d: 查看所有紀錄ID" % DeleteRecordOption.ALL)
        print("%d: 查看指定日期紀錄ID" % DeleteRecordOption.DATE)
        print("%d: 回到上一頁" % DeleteRecordOption.BACK)

    def choose(self):
        while True:
            try:
                option = DeleteRecordOption(int(input()))
                break
            except ValueError:
                print(self.errorMsg)
        return option

    def execute(self,option):
        if option is DeleteRecordOption.ALL:
            self.deleteByAll()
        elif option is DeleteRecordOption.DATE:
            self.deleteByDate()
        else:
            raise ValueError(self.errorMsg)
    
    def format_print(self, results):
        for row in results:
            dictRow = row._asdict()
            print(dictRow['id'], "\t", dictRow['category'],"\t",dictRow['amount'],"\t", dictRow['payment'],"\t", dictRow['place'].decode("utf-8"),"\t", dictRow['time'])
            
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
        deletedRows = resultProxy.rowcount
        if (deletedRows != 1):
            print("此紀錄ID不存在")
        self.tearDown_connection()

    def deleteByAll(self):
        self.setUp_connection_and_table()
        query = sql.select(self.table)
        results = self.conn.execute(query).fetchall()
        self.tearDown_connection()
        self.format_print(results)
        self.deleteByID()

    def deleteByDate(self):
        Date = input("請輸入想要看的日期(yyyy-mm-dd): ")
        self.setUp_connection_and_table()
        query = sql.select(self.table).where(self.table.c.time == Date)
        results = self.conn.execute(query).fetchall()
        self.tearDown_connection()
        self.format_print(results)
        self.deleteByID()

    def start(self):
        while True:
            self.show()
            option = self.choose()
            if option is DeleteRecordOption.BACK:
                return
            self.execute(option)

if __name__ == '__main__':  # pragma: no cover
    deleteRecordPage = DeleteRecordPage()
    deleteRecordPage.start()