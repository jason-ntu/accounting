from enum import IntEnum, auto

class AddRecordOption(IntEnum):
    FOOD = auto()
    DRINK = auto()
    BACK = auto()

class PaymentOption(IntEnum):
    CREDITCARD = auto()
    OTHER = auto()
    BACK = auto()

class AddRecordPage:

    errorMsg = "請輸入 1 到 3 之間的數字:"

    def show(self):
        print("%d: 新增食物類別" % AddRecordOption.FOOD)
        print("%d: 新增飲料類別" % AddRecordOption.DRINK)
        print("%d: 回到上一頁" % AddRecordOption.BACK)

    def choose(self):
        while True:
            try:
                option = AddRecordOption(int(input()))
                break
            except ValueError:
                print(self.errorMsg)
        return option

    def choosePayment(self):
        print("%d: 信用卡支付" % PaymentOption.CREDITCARD)
        print("%d: 其他" % PaymentOption.OTHER)
        print("%d: 回到上一頁" % PaymentOption.BACK)
        while True:
            try:
                option = PaymentOption(int(input()))
                break
            except ValueError:
                print(self.errorMsg)
        return option

    def execute(self,option):
        if option is AddRecordOption.FOOD:
            self.addFood()
        elif option is AddRecordOption.DRINK:
            self.addDrink()
        else:
            raise ValueError(self.errorMsg)

    def addFood(self):  # pragma: no cover
        # 確認流程是否正確
        # 選擇類別->選擇支付方式->輸入金額
        option = self.choosePayment()
        if option is AddRecordOption.BACK:
            return
        print("請輸入金額")
        amountOfMoney = int(input())
        pass

    def addDrink(self):  # pragma: no cover
        pass

    def start(self):
        while True:
            self.show()
            option = self.choose()
            if option is AddRecordOption.BACK:
                return
            self.execute(option)

if __name__ == '__main__':  # pragma: no cover
    addRecordPage = AddRecordPage()
    addRecordPage.start()
