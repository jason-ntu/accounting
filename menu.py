from records import showRecordsPage
from reports import showReportsPage
from export import showExportPage
from setting import showSettingPage

# 進入選單
def showMenu():
    option = input("請輸入選項")
    if option == '消費紀錄':
        showRecordsPage()
    elif option == '查看報表':
        showReportsPage()
    elif option == '輸出':
        showExportPage()
    elif option == '設定':
        showSettingPage()
    else:
        print("輸入錯誤")
    pass

# > 消費紀錄 Records
# > 查看報表 Reports
# > 輸出 Export
# > 設定 Settings