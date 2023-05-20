from enum import IntEnum, auto, Enum
from records import RecordPage
from report import ReportPage
#from export import ExportPage
from setting import SettingPage

class MenuOption(IntEnum):
    RECORD = auto()
    REPORT = auto()
    EXPORT = auto()
    SETTING = auto()
    CLOSE = auto()

class MenuText():
    RECORD = ('%d: 消費紀錄' % MenuOption.RECORD)
    REPORT = ('%d: 查看報表' % MenuOption.REPORT)
    EXPORT = ('%d: 匯出資料' % MenuOption.EXPORT)
    SETTING = ('%d: 基本設定' % MenuOption.SETTING)
    CLOSE = ('%d: 關閉程式' % MenuOption.CLOSE)
    TITLE = '========== 記帳簿［首頁］ =========='
    SUBTITLE = '［首頁］'
    QUESTION = '請選擇功能：'
    HINT = '輸入錯誤，請重新輸入！'

class MenuPage:
    #進入點
    def start(self):
        while True:
            self.show()
            option = self.choose()
            if option is MenuOption.CLOSE:
                return
            self.execute(option)

    #呈現選擇畫面
    def show(self):
        print(MenuText.TITLE)
        print(MenuText.RECORD)
        print(MenuText.REPORT)
        print(MenuText.EXPORT)
        print(MenuText.SETTING)
        print(MenuText.CLOSE)
        print(MenuText.TITLE)

    #取得使用者選擇值
    def choose(self):
            while True:
                try:
                    option = MenuOption(int(input(MenuText.QUESTION)))
                    break
                except ValueError:
                    print(MenuText.HINT)
            return option
    
    #前往下一頁
    def execute(self, option):
        if option == MenuOption.RECORD:
            next = RecordPage()
        elif option == MenuOption.REPORT:
            next = ReportPage()
        elif option == MenuOption.EXPORT:
            pass
            #next = ExportPage()
        else:
            next = SettingPage()
        
        next.start()


if __name__ == '__main__': # pragma: no cover
    menuPage = MenuPage()
    menuPage.start()