from enum import IntEnum, auto
from datetime import datetime
import sqlalchemy as sql
from sqlalchemy import and_
from accessor import Accessor, ExecutionStatus as es

class ReportOption(IntEnum):
    CHOOSE = auto()
    BACK = auto()

class ReportByOption(IntEnum):
    category = auto()
    payment = auto()

class ReportPage(Accessor):

    table_name = "Record"

    @staticmethod
    def show():
        print("[報表]")
        print("%d: 選擇欲查詢的區間" % ReportOption.CHOOSE)
        print("%d: 回到上一頁" % ReportOption.BACK)

    @staticmethod
    def choose():
        while True:
            try:
                option = ReportOption(int(input()))
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
                return cls.chooseReportType(startDate, endDate)
                break

    @staticmethod
    def hint_start_date():
        print("請輸入\"起始\"日期 (yyyy-mm-dd):")

    @staticmethod
    def hint_finish_date():
        print("請輸入\"結束\"日期 (yyyy-mm-dd):")

    @classmethod
    def chooseReportType(cls, startDate, endDate):
        cls.hint_choose_report_type()
        while True:
            try:
                _type = ReportByOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 2 之間的數字:")
                return False
        return cls.Report(startDate, endDate, _type)

    @staticmethod
    def hint_choose_report_type():
        print("報表顯示類型(1 依\"類別\" 2 \"依支付方式\"):")

    @classmethod
    def Report(cls, startDate, endDate, _type):
        query = sql.select(cls.table).where(and_(cls.table.c.time >= startDate, cls.table.c.time <= endDate))
        results = cls.conn.execute(query).fetchall()

        report_dict = {}
        total_amount = 0

        for row in results:
            dictRow = row._asdict()
            report_type = dictRow[_type.name]
            amount = dictRow['amount']

            if report_type in report_dict:
                report_dict[report_type] += amount
            else:
                report_dict[report_type] = amount
            total_amount += amount

        percentage_totals = 0
        percentages = []
        for report_type, amount in report_dict.items():
            percentage = (amount / total_amount) * 100
            percentage = round(percentage)
            percentage_totals += percentage
            percentages.append(percentage)
            last_percentage = percentage

        if percentage_totals != 100:
            last_percentage = 100 - percentage_totals + percentages[-1]
            percentages[-1] = last_percentage

        for report_type, amount, percentage in zip(report_dict.keys(), report_dict.values(), percentages):
            print(f"\"{report_type}\" 金額總和:{amount} 百分比:{percentage}%")

        print(f"金額總和:{total_amount} 百分比:{sum(percentages)}%")
        return True

    @classmethod
    def start(cls):
        while True:
            cls.show()
            option = cls.choose()
            if option is ReportOption.BACK:
                return
            cls.execute(option)

if __name__ == '__main__': # pragma: no cover
    settingsPage = ReportPage()
    settingsPage.start()
