from enum import IntEnum, auto
from datetime import datetime
import sqlalchemy as sql
from accessor import Accessor
from sqlalchemy import and_

class UpdateRecordOption(IntEnum):
    ALL = auto()
    DATE = auto()
    BACK = auto()

class CategoryOption(IntEnum):
    category = auto()
    payment = auto()
    amount = auto()
    place = auto()
    time = auto()

class UpdateRecordPage(Accessor):

    errorMsg = "請輸入 1 到 3 之間的數字: "
    table_name = "Record"
    IDerrorMsg = "輸入的ID須為整數"
    CategoryerrorMsg = "請輸入 1 到 5 之間的數字: "

    def show(self):
        print("%d: 查看所有紀錄ID" % UpdateRecordOption.ALL)
        print("%d: 查看指定日期紀錄ID" % UpdateRecordOption.DATE)
        print("%d: 回到上一頁" % UpdateRecordOption.BACK)

    def choose(self):
        while True:
            try:
                option = UpdateRecordOption(int(input()))
                break
            except ValueError:
                print(self.errorMsg)
        return option

    def execute(self,option):
        if option is UpdateRecordOption.DATE:
            self.updateByDate()
        elif option is UpdateRecordOption.ALL:
            self.updateByALL()
        else:
            raise ValueError(self.errorMsg)
    def format_print(self, results):
        for row in results:
            dictRow = row._asdict()
            print(dictRow['id'], "\t", dictRow['category'],"\t",dictRow['amount'],"\t", dictRow['payment'],"\t", dictRow['place'].decode("utf-8"),"\t", dictRow['time'])
    
    def chooseCategory(self):
        while True:
            try:
                option = CategoryOption(int(input()))
                break
            except ValueError:
                print(self.CategoryerrorMsg)
        return option
    
    def checkIDInteger(self):
        while True:
            try:
                ID = int(input("請輸入想更改的紀錄ID: "))
                break
            except ValueError:
                print(self.IDerrorMsg)
        return ID

    def updateDB(self, option):
        if option is UpdateRecordOption.DATE:
            self.updateByDate()
        elif option is UpdateRecordOption.ALL:
            self.updateByALL()
        else:
            raise ValueError(self.errorMsg)

    def updateByID(self):  # pragma: no cover
        ID = self.checkIDInteger()
        self.setUp_connection_and_table()
        option = self.chooseCategory()
        self.updateDB(option)

    def updateByDate(self):  # pragma: no cover
        pass

    def updateByALL(self):  # pragma: no cover
        self.setUp_connection_and_table()
        query = sql.select(self.table)
        results = self.conn.execute(query).fetchall()
        self.tearDown_connection()
        self.format_print(results)
        self.updateByID()

    def start(self):
        while True:
            self.show()
            option = self.choose()
            if option is UpdateRecordOption.BACK:
                return
            self.execute(option)

if __name__ == '__main__':  # pragma: no cover
    updateRecordPage = UpdateRecordPage()
    updateRecordPage.start()