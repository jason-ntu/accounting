from enum import IntEnum, auto
from datetime import datetime
class ViewRecordOption(IntEnum):
    TODAY = auto()
    WEEK = auto()
    MONTH = auto()
    OTHER = auto()
    BACK = auto()

class ViewRecordPage:

    errorMsg = "請輸入 1 到 5 之間的數字:"

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
        # 呼叫報表function？
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

    def viewToday(self):  # pragma: no cover
        pass

    def viewWeek(self):  # pragma: no cover
        pass

    def viewMonth(self):  # pragma: no cover
        pass

    def viewOther(self):  # pragma: no cover
        pass

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