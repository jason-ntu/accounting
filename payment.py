from enum import IntEnum, auto
import utils

class PaymentOption(IntEnum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()
    BACK = auto()

class PaymentCategory(IntEnum):
    CASH = auto()
    DEBIT_CARD = auto()
    CREDIT_CARD = auto()
    ELECTRONIC = auto()
    OTHER = auto()

class Payment:
    name: str
    balance: int
    category: PaymentCategory

class PaymentPage:

    def show(self):
        print("%d: 新增支付方式" % PaymentOption.READ)
        print("%d: 查看支付方式" % PaymentOption.READ)
        print("%d: 修改支付方式" % PaymentOption.READ)
        print("%d: 刪除支付方式" % PaymentOption.UPDATE)
        print("%d: 回到上一頁" % PaymentOption.BACK)

    def choose(name):
        while True:
            try:
                option = PaymentOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 5 之間的數字:")
        return option

    def execute(self,option):
        if option is PaymentOption.CREATE:
            self.create()
        elif option is PaymentOption.READ:
            self.read()
        elif option is PaymentOption.UPDATE:
            self.update()
        elif option is PaymentOption.DELETE:
            self.delete()
        
    def create(self, name):
        self.hint_create_name()
        name = input()
        self.hint_create_balance()
        while True:
            try:
                balance = float(input())
                break
            except ValueError:
                print("請輸入數字:")
        self.hint_create_category()
        while True:
            try:
                category = PaymentCategory(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 5 之間的數字:")
        return utils.db_write("""INSERT INTO `payment_table` (`name`, `balance`, `category`) VALUES ('%s', '%f', '%s')""" % (name, balance, category.name))

    def hint_create_name(self):
        print("請輸入新支付方式的...")
        print("名稱:")
    
    def hint_create_balance(self):
        print("餘額:")
    
    def hint_create_category(self):
        print("類型(1 現金, 2 借記卡, 3 信用卡, 4 電子支付, 5 其他):")

    def read(self, name):
        pass
    
    def update(self, name, newName):
        pass

    def delete(self, name):
        pass

    def start(self):
        while True:
            self.show()
            option = self.choose()
            if option is PaymentOption.BACK:
                return
            self.execute(option)

if __name__ == '__main__':  # pragma: no cover
    budgetPage = PaymentPage()
    budgetPage.start()