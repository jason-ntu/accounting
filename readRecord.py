from enum import IntEnum, auto
from datetime import datetime, timedelta
from accessor import Accessor
import sqlalchemy as sql
from sqlalchemy import and_
import sys


class ReadRecordOption(IntEnum):
    TODAY = auto()
    WEEK = auto()
    MONTH = auto()
    OTHER = auto()
    BACK = auto()

class ReadRecordPage(Accessor):

    errorMsg = "請輸入 1 到 5 之間的數字:"
    table_name = "Record"

    def show(self):
        print("%d: 查看本日紀錄" % ReadRecordOption.TODAY)
        print("%d: 查看本週紀錄" % ReadRecordOption.WEEK)
        print("%d: 查看本月紀錄" % ReadRecordOption.MONTH)
        print("%d: 查看指定時間紀錄" % ReadRecordOption.OTHER)
        print("%d: 回到上一頁" % ReadRecordOption.BACK)

    def choose(self):
        while True:
            try:
                option = ReadRecordOption(int(input()))
                break
            except ValueError:
                print(self.errorMsg)
        return option

    def execute(self,option):
        if option is ReadRecordOption.TODAY:
            self.viewToday()
        elif option is ReadRecordOption.WEEK:
            self.viewWeek()
        elif option is ReadRecordOption.MONTH:
            self.viewMonth()
        elif option is ReadRecordOption.OTHER:
            self.viewOther()
        else:
            raise ValueError(self.errorMsg)
        
    def recordFormatPrint(self, results):
        for row in results:
            dictRow = row._asdict() 
            print(dictRow['id']," 類別:", dictRow['category']," 金額:", dictRow['amount']," 支付方式:", dictRow['payment']," 地點:", dictRow['place'], " 時間:", dictRow['time'])

    def viewToday(self):  # pragma: no cover
        Date = datetime.today().date()
        self.setUp_connection_and_table()
        query = sql.select(self.table).where(self.table.c.time == Date)
        results = self.conn.execute(query).fetchall()
        self.tearDown_connection()
        self.recordFormatPrint(results)

    def viewWeek(self):  # pragma: no cover
        Date = datetime.today().date()
        startDate = Date - timedelta(days=Date.weekday())
        endDate = startDate + timedelta(days=6)
        self.setUp_connection_and_table()
        query = sql.select(self.table).where(and_(self.table.c.time >= startDate, self.table.c.time <= endDate))
        results = self.conn.execute(query).fetchall()
        self.tearDown_connection()
        self.recordFormatPrint(results)

    def viewMonth(self):  # pragma: no cover
        Date = datetime.today().date()
        startDate = datetime(Date.year, Date.month, 1).date()
        nextMonth = Date.replace(day=28) + timedelta(days=4)
        endDate = nextMonth - timedelta(days=nextMonth.day)
        self.setUp_connection_and_table()
        query = sql.select(self.table).where(and_(self.table.c.time >= startDate, self.table.c.time <= endDate))
        results = self.conn.execute(query).fetchall()
        self.tearDown_connection()
        self.recordFormatPrint(results)

    def viewOther(self):  # pragma: no cover
        startDate = str(input("請輸入 開始 時間(yyyy-mm-dd): "))
        endDate = str(input("請輸入 結束 時間(yyyy-mm-dd): "))
        self.setUp_connection_and_table()
        query = sql.select(self.table).where(and_(self.table.c.time >= startDate, self.table.c.time <= endDate))
        results = self.conn.execute(query).fetchall()
        self.tearDown_connection()
        self.recordFormatPrint(results)

    def start(self):
        while True:
            self.show()
            option = self.choose()
            if option is ReadRecordOption.BACK:
                return
            self.execute(option)

if __name__ == '__main__':  # pragma: no cover
    readRecordPage = ReadRecordPage()
    readRecordPage.start()