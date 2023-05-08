from enum import IntEnum, auto

class DeleteRecordOption(IntEnum):
    DATE = auto()
    CATEGORY = auto()
    BACK = auto()

class DeleteRecordPage:

    errorMsg = "請輸入 1 到 3 之間的數字:"

    def show(self):
        print("%d: 依據日期刪除紀錄" % DeleteRecordOption.DATE)
        print("%d: 依據類別刪除紀錄" % DeleteRecordOption.CATEGORY)
        print("%d: 回到上一頁" % DeleteRecordOption.BACK)

    def choose(self):
        while True:
            try:
                option = DeleteRecordOption(int(input()))
                break
            except ValueError:
                print(self.errorMsg)
        return option

    def execute(self,option):
        if option is DeleteRecordOption.DATE:
            self.deleteByDate()
        elif option is DeleteRecordOption.CATEGORY:
            self.deleteByCategory()
        else:
            raise ValueError(self.errorMsg)

    def deleteByDate(self):  # pragma: no cover
        pass

    def deleteByCategory(self):  # pragma: no cover
        pass

    def start(self):
        while True:
            self.show()
            option = self.choose()
            if option is DeleteRecordOption.BACK:
                return
            self.execute(option)

if __name__ == '__main__':  # pragma: no cover
    deleteRecordPage = DeleteRecordPage()
    deleteRecordPage.start()