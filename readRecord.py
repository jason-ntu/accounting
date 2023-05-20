from enum import IntEnum, auto
from datetime import datetime, timedelta
from accessor import Accessor, ExecutionStatus as es
import sqlalchemy as sql
from sqlalchemy import and_
from records import RecordPage
import sys


class ReadRecordOption(IntEnum):
    TODAY = auto()
    WEEK = auto()
    MONTH = auto()
    OTHER = auto()
    BACK = auto()

class ReadRecordPage(RecordPage):

    @staticmethod
    def show():
        print("%d: 查看本日紀錄" % ReadRecordOption.TODAY)
        print("%d: 查看本週紀錄" % ReadRecordOption.WEEK)
        print("%d: 查看本月紀錄" % ReadRecordOption.MONTH)
        print("%d: 查看指定時間紀錄" % ReadRecordOption.OTHER)
        print("%d: 回到上一頁" % ReadRecordOption.BACK)
    
    @staticmethod
    def hintGetStartDate():
        print("請輸入 開始 時間(yyyy-mm-dd): ")
    
    @staticmethod
    def hintGetEndDate():
        print("請輸入 結束 時間(yyyy-mm-dd): ")

    @staticmethod
    def choose():
        while True:
            try:
                option = ReadRecordOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 5 之間的數字:")
        return option

    @classmethod
    def execute(cls, option):
        if option is ReadRecordOption.TODAY:
            cls.viewToday()
        elif option is ReadRecordOption.WEEK:
            cls.viewWeek()
        elif option is ReadRecordOption.MONTH:
            cls.viewMonth()
        else :
            cls.viewOther()
    
    @classmethod
    def viewToday(clf):  
        Date = datetime.today().date()
        clf.setUp_connection_and_table()
        query = sql.select(clf.table).where(clf.table.c.consumptionDate == Date)
        results = clf.conn.execute(query).fetchall()
        clf.tearDown_connection(es.NONE)
        for row in results:
            dictRow = row._asdict() 
            print(dictRow['id'], dictRow['IE']," 類別:", dictRow['category']," 金額:", 
                  dictRow['amount']," 收支方式:", dictRow['payment']," 地點:", dictRow['place'], 
                  " 消費時間:", dictRow['consumptionDate'], " 扣款時間:", dictRow['deductionDate'],
                  " 發票號碼:", dictRow['invoice'], " 備註:", dictRow['note'])


    @classmethod
    def viewWeek(clf):  
        Date = datetime.today().date()
        startDate = Date - timedelta(days=Date.weekday())
        endDate = startDate + timedelta(days=6)
        clf.setUp_connection_and_table()
        query = sql.select(clf.table).where(and_(clf.table.c.consumptionDate >= startDate, clf.table.c.consumptionDate <= endDate))
        results = clf.conn.execute(query).fetchall()
        clf.tearDown_connection(es.NONE)
        for row in results:
            dictRow = row._asdict() 
            print(dictRow['id'], dictRow['IE']," 類別:", dictRow['category']," 金額:", 
                  dictRow['amount']," 收支方式:", dictRow['payment']," 地點:", dictRow['place'], 
                  " 消費時間:", dictRow['consumptionDate'], " 扣款時間:", dictRow['deductionDate'],
                  " 發票號碼:", dictRow['invoice'], " 備註:", dictRow['note'])


    @classmethod
    def viewMonth(clf): 
        Date = datetime.today().date()
        startDate = datetime(Date.year, Date.month, 1).date()
        nextMonth = Date.replace(day=28) + timedelta(days=4)
        endDate = nextMonth - timedelta(days=nextMonth.day)
        clf.setUp_connection_and_table()
        query = sql.select(clf.table).where(and_(clf.table.c.consumptionDate >= startDate, clf.table.c.consumptionDate <= endDate))
        results = clf.conn.execute(query).fetchall()
        clf.tearDown_connection(es.NONE)
        for row in results:
            dictRow = row._asdict() 
            print(dictRow['id'], dictRow['IE']," 類別:", dictRow['category']," 金額:", 
                  dictRow['amount']," 收支方式:", dictRow['payment']," 地點:", dictRow['place'], 
                  " 消費時間:", dictRow['consumptionDate'], " 扣款時間:", dictRow['deductionDate'],
                  " 發票號碼:", dictRow['invoice'], " 備註:", dictRow['note'])

    @classmethod
    def viewOther(clf):  
        clf.hintGetStartDate()
        startDate = str(input())
        clf.hintGetEndDate()
        endDate = str(input())
        clf.setUp_connection_and_table()
        query = sql.select(clf.table).where(and_(clf.table.c.consumptionDate >= startDate, clf.table.c.consumptionDate <= endDate))
        results = clf.conn.execute(query).fetchall()
        clf.tearDown_connection(es.NONE)
        for row in results:
            dictRow = row._asdict() 
            print(dictRow['id'], dictRow['IE']," 類別:", dictRow['category']," 金額:", 
                  dictRow['amount']," 收支方式:", dictRow['payment']," 地點:", dictRow['place'], 
                  " 消費時間:", dictRow['consumptionDate'], " 扣款時間:", dictRow['deductionDate'],
                  " 發票號碼:", dictRow['invoice'], " 備註:", dictRow['note'])


    @classmethod
    def start(clf):
        while True:
            clf.show()
            option = clf.choose()
            if option is ReadRecordOption.BACK:
                return
            clf.execute(option)

if __name__ == '__main__':  # pragma: no cover
    readRecordPage = ReadRecordPage()
    readRecordPage.start()