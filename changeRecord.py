from enum import IntEnum, auto

class ChangeRecordOption(IntEnum):
    DATE = auto()
    CATEGORY = auto()
    BACK = auto()

class ChangeRecordPage:

    errorMsg = "請輸入 1 到 3 之間的數字:"

    def show(self):
        print("%d: 依據日期修改紀錄" % ChangeRecordOption.DATE)
        print("%d: 依據類別修改紀錄" % ChangeRecordOption.CATEGORY)
        print("%d: 回到上一頁" % ChangeRecordOption.BACK)

    def choose(self):
        while True:
            try:
                option = ChangeRecordOption(int(input()))
                break
            except ValueError:
                print(self.errorMsg)
        return option

    def execute(self,option):
        if option is ChangeRecordOption.DATE:
            self.changeByDate()
        elif option is ChangeRecordOption.CATEGORY:
            self.changeByCategory()
        else:
            raise ValueError(self.errorMsg)

    def changeByDate(self):  # pragma: no cover
        pass

    def changeByCategory(self):  # pragma: no cover
        pass

    def start(self):
        while True:
            self.show()
            option = self.choose()
            if option is ChangeRecordOption.BACK:
                return
            self.execute(option)

if __name__ == '__main__':  # pragma: no cover
    changeRecordPage = ChangeRecordPage()
    changeRecordPage.start()