from enum import IntEnum, auto
from datetime import datetime
import sqlalchemy as sql
from sqlalchemy import and_
from accessor import Accessor, ExecutionStatus as es
from openpyxl import Workbook

class ExportOption(IntEnum):
    CHOOSE = auto()
    BACK = auto()

class ExportPage(Accessor):

    table_name = "Record"

    @staticmethod
    def show():
        print("%d: 選擇欲匯出的區間" % ExportOption.CHOOSE)
        print("%d: 回到上一頁" % ExportOption.BACK)

    @staticmethod
    def choose():
        while True:
            try:
                option = ExportOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 2 之間的數字:")
        return option

    @classmethod
    def execute(cls, option):
        cls.setUp_connection_and_table()
        successful = cls.chooseInterval()
        if successful:
            cls.tearDown_connection(es.COMMIT)
        else:
            cls.tearDown_connection(es.ROLLBACK)

    @classmethod
    def chooseInterval(cls):
        print("起始日期 00:00:00 到結束日期 23:59:59")
        while True:
            cls.hint_start_date()
            startDate_str = input()
            cls.hint_finish_date()
            endDate_str = input()
            try:
                startDate = datetime.strptime(startDate_str, "%Y-%m-%d")
                endDate = datetime.strptime(endDate_str, "%Y-%m-%d")
            except ValueError:
                print("Error: 日期格式錯誤")
                break

            if endDate < startDate:
                print("Error: 時間區間至少一天")
                break
            else:
                return cls.inputFileName(startDate, endDate)
                break

    @staticmethod
    def hint_start_date():
        print("請輸入\"起始\"日期 (yyyy-mm-dd):")

    @staticmethod
    def hint_finish_date():
        print("請輸入\"結束\"日期 (yyyy-mm-dd):")

    @classmethod
    def inputFileName(cls, startDate, endDate):
        cls.hint_input_filename()
        filename = input()
        return cls.exportFile(startDate, endDate, filename)

    @staticmethod
    def hint_input_filename():
        print("請輸入檔案名稱:")

    @classmethod
    def exportFile(cls, startDate, endDate, filename):
        query = sql.select(cls.table).where(and_(cls.table.c.purchaseDate >= startDate, cls.table.c.debitDate <= endDate))
        results = cls.conn.execute(query).fetchall()
        workbook = Workbook()
        worksheet = workbook.active

        worksheet.append(["IE", "category", "account", "amount", "location", "purchaseDate", "debitDate", "invoice", "note"])

        for row in results:
            worksheet.append([row.IE, row.category, row.account, row.amount, row.location, row.purchaseDate, row.debitDate, row.invoice, row.note])

        workbook.save(filename + ".xlsx")

        return True

    @classmethod
    def start(cls):
        while True:
            cls.show()
            option = cls.choose()
            if option is ExportOption.BACK:
                return
            cls.execute(option)