from enum import IntEnum, auto
from datetime import datetime

class ReportOption(IntEnum):
    CHOOSE = auto()
    BACK = auto()

class ReportPage:

    def show(self):
        print("[報表]")
        print("%d: 選擇欲查詢的區間" % ReportOption.CHOOSE)
        print("%d: 回到上一頁" % ReportOption.BACK)

    def chooseInterval(self):
        while True:
            startDate_str = input("請輸入\"起始\"日期 (yyyy-mm-dd): ")
            endDate_str = input("請輸入\"結束\"日期 (yyyy-mm-dd): ")
            try:
                startDate = datetime.strptime(startDate_str, "%Y-%m-%d")
                endDate = datetime.strptime(endDate_str, "%Y-%m-%d")
            except ValueError:
                print("Error: 日期格式錯誤")
                print("---------------------")
                break

            if endDate <= startDate:
                print("Error: 時間區間至少一天")
                print("---------------------")
                break
            else:
                self.Report(startDate,endDate)
                break

    def Report(self, startDate, endDate):
        pass

    def choose(self):
        while True:
            try:
                option = ReportOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 2 之間的數字:")
        return option

    def start(self):
        while True:
            self.show()
            option = self.choose()
            if option is ReportOption.BACK:
                return
            self.chooseInterval()

if __name__ == '__main__': # pragma: no cover
    settingsPage = ReportPage()
    settingsPage.start()
