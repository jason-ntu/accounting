from enum import IntEnum, auto
from datetime import datetime, timedelta
from accessor import Accessor
import sqlalchemy as sql
from sqlalchemy import and_
import sys


class ViewRecordOption(IntEnum):
    TODAY = auto()
    WEEK = auto()
    MONTH = auto()
    OTHER = auto()
    BACK = auto()

class ViewRecordPage(Accessor):

    errorMsg = "請輸入 1 到 5 之間的數字:"
    table_name = "Record"

    def show(self):
        print("%d: 查看本日紀錄" % ViewRecordOption.TODAY)
        print("%d: 查看本週紀錄" % ViewRecordOption.WEEK)
        print("%d: 查看本月紀錄" % ViewRecordOption.MONTH)
        print("%d: 查看指定時間紀錄" % ViewRecordOption.OTHER)
        print("%d: 回到上一頁" % ViewRecordOption.BACK)

    def choose(self):
        while True:
            try:
                option = ViewRecordOption(int(input()))
                break
            except ValueError:
                print(self.errorMsg)
        return option

    def execute(self,option):
        if option is ViewRecordOption.TODAY:
            self.viewToday()
        elif option is ViewRecordOption.WEEK:
            self.viewWeek()
        elif option is ViewRecordOption.MONTH:
            self.viewMonth()
        elif option is ViewRecordOption.OTHER:
            self.viewOther()
        else:
            raise ValueError(self.errorMsg)
        
    def format_print(self, results):
        print("類別\t金額\t方式\t場所\t時間\t")
        for row in results:
            dictRow = row._asdict() 
            print(dictRow['category'],"\t",dictRow['amount'],"\t", dictRow['payment'],"\t", dictRow['place'].decode("utf-8"),"\t", dictRow['time'])

    def viewToday(self):  # pragma: no cover
        Date = datetime.today().date()
        self.setUp_connection_and_table()
        query = sql.select(self.table.c["amount", "category", "payment", "place", "time"]).where(self.table.c.time == Date)
        results = self.conn.execute(query).fetchall()
        self.tearDown_connection()
        self.format_print(results)

    def viewWeek(self):  # pragma: no cover
        Date = datetime.today().date()
        startDate = Date - timedelta(days=Date.weekday())
        endDate = startDate + timedelta(days=6)
        self.setUp_connection_and_table()
        query = sql.select(self.table.c["amount", "category", "payment", "place", "time"]).where(and_(self.table.c.time >= startDate, self.table.c.time <= endDate))
        results = self.conn.execute(query).fetchall()
        self.tearDown_connection()
        self.format_print(results)

    def viewMonth(self):  # pragma: no cover
        Date = datetime.today().date()
        startDate = datetime(Date.year, Date.month, 1)
        nextMonth = Date.replace(day=28) + timedelta(days=4)
        endDate = nextMonth - timedelta(days=nextMonth.day)
        self.setUp_connection_and_table()
        query = sql.select(self.table.c["amount", "category", "payment", "place", "time"]).where(and_(self.table.c.time >= startDate, self.table.c.time <= endDate))
        results = self.conn.execute(query).fetchall()
        self.tearDown_connection()
        self.format_print(results)

    def viewOther(self):  # pragma: no cover
        startDate = str(input("請輸入 開始 時間(yyyy-mm-dd): "))
        endDate = str(input("請輸入 結束 時間(yyyy-mm-dd): "))
        self.setUp_connection_and_table()
        query = sql.select(self.table.c["amount", "category", "payment", "place", "time"]).where(and_(self.table.c.time >= startDate, self.table.c.time <= endDate))
        results = self.conn.execute(query).fetchall()
        self.tearDown_connection()
        self.format_print(results)

    def start(self):
        while True:
            self.show()
            option = self.choose()
            if option is ViewRecordOption.BACK:
                return
            self.execute(option)

if __name__ == '__main__':  # pragma: no cover
    viewRecordPage = ViewRecordPage()
    viewRecordPage.start()