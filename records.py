from enum import IntEnum, auto
from readRecord import ReadRecordPage
from deleteRecord import DeleteRecordPage
from createRecord import CreateRecordPage
from updateRecord import UpdateRecordPage


# 消費紀錄 Records
# > 新增消費紀錄
# > 檢視消費紀錄 
# > 修改消費紀錄
# > 刪除消費紀錄

class RecordOption(IntEnum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()
    BACK = auto()

class RecordPage:
    # 消費紀錄 Records
    def choose(self):
        while True:
            try:
                option = RecordOption(int(input()))
                break
            except ValueError:
                print(self.errorMsg)
        return option

    
    def start(self):
        while True:
            self.show()
            option = self.choose()
            if option is RecordOption.BACK:
                return
            self.enter(option)

    def show(self):
        print("%d: 新增消費紀錄" % RecordOption.CREATE)
        print("%d: 檢視消費紀錄" % RecordOption.READ)
        print("%d: 修改消費紀錄" % RecordOption.UPDATE)
        print("%d: 刪除消費紀錄" % RecordOption.DELETE)
        print("%d: 回到上一頁" % RecordOption.BACK)

    def enter(self, option):
        if option is RecordOption.CREATE:
            nextPage = CreateRecordPage()
        elif option is RecordOption.READ:
            nextPage = ReadRecordPage()
        elif option is RecordOption.UPDATE:
            nextPage = UpdateRecordPage()
        elif option is RecordOption.DELETE:
            nextPage = DeleteRecordPage()
        else:
            raise ValueError(self.errorMsg)
        nextPage.start()

if __name__ == '__main__': # pragma: no cover
    recordPage = RecordPage()
    recordPage.start()
