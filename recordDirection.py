from enum import IntEnum, auto

class RecordDirection(IntEnum):
    INCOME = auto()
    EXPENSE = auto()

def askIE():
    hintGetIE()
    while True:
        try:
            IE = RecordDirection(int(input()))
            break
        except ValueError:
            print("請輸入 1 到 2 之間的數字:")
    return IE

def hintGetIE():
    print("%d: 收入" % RecordDirection.INCOME)
    print("%d: 支出" % RecordDirection.EXPENSE)