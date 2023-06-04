from enum import IntEnum, auto
from datetime import datetime, timedelta
from accessor import ExecutionStatus as es
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
        print("請輸入 開始 時間(yyyy-mm-dd):")
    
    @staticmethod
    def hintGetEndDate():
        print("請輸入 結束 時間(yyyy-mm-dd):")

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
    def viewToday(cls):  
        Date = datetime.today().date()
        cls.setUp_connection_and_table()
        query = sql.select(cls.table).where(cls.table.c.purchaseDate == Date)
        results = cls.conn.execute(query).fetchall()
        cls.tearDown_connection(es.NONE)
        for row in results:
            dictRow = row._asdict() 
            print(dictRow['id'], dictRow['IE']," 類別:", dictRow['category']," 金額:", 
                  dictRow['amount']," 帳戶:", dictRow['account']," 地點:", dictRow['location'], 
                  " 消費時間:", dictRow['purchaseDate'], " 扣款時間:", dictRow['debitDate'],
                  " 發票號碼:", dictRow['invoice'], " 備註:", dictRow['note'])


    @classmethod
    def viewWeek(cls):  
        Date = datetime.today().date()
        startDate = Date - timedelta(days=Date.weekday())
        endDate = startDate + timedelta(days=6)
        cls.setUp_connection_and_table()
        query = sql.select(cls.table).where(and_(cls.table.c.purchaseDate >= startDate, cls.table.c.purchaseDate <= endDate))
        results = cls.conn.execute(query).fetchall()
        cls.tearDown_connection(es.NONE)
        for row in results:
            dictRow = row._asdict() 
            print(dictRow['id'], dictRow['IE']," 類別:", dictRow['category']," 金額:", 
                  dictRow['amount']," 帳戶:", dictRow['account']," 地點:", dictRow['location'], 
                  " 消費時間:", dictRow['purchaseDate'], " 扣款時間:", dictRow['debitDate'],
                  " 發票號碼:", dictRow['invoice'], " 備註:", dictRow['note'])


    @classmethod
    def viewMonth(cls): 
        Date = datetime.today().date()
        startDate = datetime(Date.year, Date.month, 1).date()
        nextMonth = Date.replace(day=28) + timedelta(days=4)
        endDate = nextMonth - timedelta(days=nextMonth.day)
        cls.setUp_connection_and_table()
        query = sql.select(cls.table).where(and_(cls.table.c.purchaseDate >= startDate, cls.table.c.purchaseDate <= endDate))
        results = cls.conn.execute(query).fetchall()
        cls.tearDown_connection(es.NONE)
        for row in results:
            dictRow = row._asdict() 
            print(dictRow['id'], dictRow['IE']," 類別:", dictRow['category']," 金額:", 
                  dictRow['amount']," 帳戶:", dictRow['account']," 地點:", dictRow['location'], 
                  " 消費時間:", dictRow['purchaseDate'], " 扣款時間:", dictRow['debitDate'],
                  " 發票號碼:", dictRow['invoice'], " 備註:", dictRow['note'])

    @classmethod
    def viewOther(cls):  
        cls.hintGetStartDate()
        while True:
            try:
                startDate = input()
                if (startDate == ""):
                    startDate = datetime.today().date()
                    break
                datetime.strptime(startDate, '%Y-%m-%d').date()
                break
            except ValueError:
                cls.hintGetStartDate()

        cls.hintGetEndDate()
        while True:
            try:
                endDate = input()
                if (endDate == ""):
                    endDate = datetime.today().date()
                    break
                datetime.strptime(endDate, '%Y-%m-%d').date()
                break
            except ValueError:
                cls.hintGetEndDate()
                
        cls.setUp_connection_and_table()
        query = sql.select(cls.table).where(and_(cls.table.c.purchaseDate >= startDate, cls.table.c.purchaseDate <= endDate))
        results = cls.conn.execute(query).fetchall()
        cls.tearDown_connection(es.NONE)
        for row in results:
            dictRow = row._asdict() 
            print(dictRow['id'], dictRow['IE']," 類別:", dictRow['category']," 金額:", 
                  dictRow['amount']," 帳戶:", dictRow['account']," 地點:", dictRow['location'], 
                  " 消費時間:", dictRow['purchaseDate'], " 扣款時間:", dictRow['debitDate'],
                  " 發票號碼:", dictRow['invoice'], " 備註:", dictRow['note'])


    @classmethod
    def start(cls):
        while True:
            cls.show()
            option = cls.choose()
            if option is ReadRecordOption.BACK:
                return
            cls.execute(option)