from enum import IntEnum, auto
# from budget import BudgetPage
# from fixedIE import FixedIE
# from category import Category
# from balance import Balance
# from location import Location

from addRecord import AddRecordPage
from viewRecord import ViewRecordPage
from changeRecord import ChangeRecordPage
from deleteRecord import DeleteRecordPage


# 消費紀錄 Records
# > 新增消費紀錄
# > 檢視消費紀錄
# > 修改消費紀錄
# > 刪除消費紀錄

class RecordOption(IntEnum):
    ADD_RECORD = auto()
    VIEW_RECORD = auto()
    CHANGE_RECORD = auto()
    DELETE_RECORD = auto()
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
        print("%d: 新增消費紀錄" % RecordOption.ADD_RECORD)
        print("%d: 檢視消費紀錄" % RecordOption.VIEW_RECORD)
        print("%d: 修改消費紀錄" % RecordOption.CHANGE_RECORD)
        print("%d: 刪除消費紀錄" % RecordOption.DELETE_RECORD)
        print("%d: 回到上一頁" % RecordOption.BACK)

    def enter(self, option):
        if option is RecordOption.ADD_RECORD:
            nextPage = AddRecordPage()
        elif option is RecordOption.VIEW_RECORD:
            nextPage = ViewRecordPage()
        elif option is RecordOption.CHANGE_RECORD:
            nextPage = ChangeRecordPage()
        elif option is RecordOption.DELETE_RECORD:
            nextPage = DeleteRecordPage()
        else:
            raise ValueError(self.errorMsg)
        nextPage.start()

if __name__ == '__main__': # pragma: no cover
    recordPage = RecordPage()
    recordPage.start()


# def createRecord(Record):
#         if Record.balanceType.category == True:
#             # 信用卡 
#             pass
#         else:
#             # 非信用卡 
#             pass

# def readRecords(query):
#     pass

# def updateRecord(Record):
#     pass

# def deleteRecord(Record):
#     pass