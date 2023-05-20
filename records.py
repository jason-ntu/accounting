from enum import IntEnum, auto
from accessor import Accessor, ExecutionStatus as es

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

class RecordPage(Accessor):

    table_name = "Record"
    categoryList = []
    
    @staticmethod
    def choose():
        while True:
            try:
                option = RecordOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 5 之間的數字:")
        return option

    @classmethod
    def start(clf):
        while True:
            clf.show()
            option = clf.choose()
            if option is RecordOption.BACK:
                return
            clf.execute(option)

    @staticmethod
    def show():
        print("%d: 新增消費紀錄" % RecordOption.CREATE)
        print("%d: 檢視消費紀錄" % RecordOption.READ)
        print("%d: 修改消費紀錄" % RecordOption.UPDATE)
        print("%d: 刪除消費紀錄" % RecordOption.DELETE)
        print("%d: 回到上一頁" % RecordOption.BACK)

    @classmethod
    def execute(cls, option):
        if option is RecordOption.CREATE:
            from createRecord import CreateRecordPage
            CreateRecordPage.start()
        elif option is RecordOption.READ:
            from readRecord import ReadRecordPage
            ReadRecordPage.start()
        elif option is RecordOption.UPDATE:
            from updateRecord import UpdateRecordPage
            UpdateRecordPage.start()
        elif option is RecordOption.DELETE:
            from deleteRecord import DeleteRecordPage
            DeleteRecordPage.start()
        # else:
        #     raise ValueError(cls.errorMsg)

    @classmethod
    def showCategory(clf):
        for i in range(len(clf.categoryList)):
            print("%d %s" % (i+1, clf.categoryList[i]))
    
    @classmethod
    def hintGetCategory(cls):
        print("請輸入 1 到 %d 之間的數字:" % len(cls.categoryList))

if __name__ == '__main__': # pragma: no cover
    RecordPage.start()
