from enum import IntEnum, auto
import sqlalchemy as sql
from accessor import ExecutionStatus as es
from records import RecordPage
from datetime import datetime
from IEDirection import IEDirection

class FixedIEOption(IntEnum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()
    BACK = auto()

class FixedIEUpdateOption(IntEnum):
    CATEGORY = auto()
    ACCOUNT = auto()
    AMOUNT = auto()
    LOCATION = auto()
    DAY = auto()
    NOTE = auto()
    BACK = auto()

class FixedIEPage(RecordPage):

    table_name = "FixedIE"

    @staticmethod
    def show():
        print("%d: 新增固定收支" % FixedIEOption.CREATE)
        print("%d: 查看固定收支" % FixedIEOption.READ)
        print("%d: 修改固定收支" % FixedIEOption.UPDATE)
        print("%d: 刪除固定收支" % FixedIEOption.DELETE)
        print("%d: 回到上一頁" % FixedIEOption.BACK)

    @staticmethod
    def choose():
        while True:
            try:
                option = FixedIEOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 5 之間的數字:")
        return option

    @classmethod
    def execute(cls, option):
        cls.setUp_connection_and_table()
        if option is FixedIEOption.CREATE:
            successful = cls.create()
        elif option is FixedIEOption.READ:
            cls.read()
            cls.tearDown_connection(es.NONE)
            return
        elif option is FixedIEOption.UPDATE:
            cls.read()
            successful = cls.update()
        else:
            cls.read()
            successful = cls.delete()
        if successful:
            cls.tearDown_connection(es.COMMIT)
        else:
            cls.tearDown_connection(es.ROLLBACK)

    @classmethod
    def create(cls):
        IE = cls.askIE()
        cls.IE = IE.name

        cls.hint_create_name(IE)
        name = input()

        category = cls.askCategory()
        account = cls.askAccount()
        amount = cls.askAmount()
        location = cls.askLocation()
        cls.hint_create_day()
        day = cls.askDay()
        note = cls.askNote()

        query = cls.table.insert().values(IE=IE.name, name=name,
                                          category=category, account=account['name'],
                                          amount=amount, location=location,
                                          day=day, note=note, registerTime=datetime.today() ,flag=False)
        rowsAffected = cls.conn.execute(query).rowcount
        return rowsAffected == 1

    @classmethod
    def askDay(cls):
        while True:
            try:
                day = int(input())
                if day in range(1, 32):
                    return day
                raise ValueError
            except ValueError:
                cls.hintDayErorMsg()

    @staticmethod
    def hintDayErorMsg():
        print("請輸入 1 到 31 之間的數字:")

    @staticmethod
    def hint_create_name(IE):
        if IE == IEDirection.INCOME:
            print("請輸入新的固定收入名稱:")
        if IE == IEDirection.EXPENSE:
            print("請輸入新的固定支出名稱:")

    @staticmethod
    def hint_create_day():
        print("請輸入每月收支日(1-31):")

    @classmethod
    def read(cls):
        query = sql.select(cls.table.c['IE', 'name', 'category', 'account', 'amount', 'location', 'day', 'note'])
        results = cls.conn.execute(query).fetchall()
        cls.format_print(results)

    @staticmethod
    def format_print(results):
        for row in results:
            dictRow = row._asdict()
            print("%s 名稱\"%s\" 類別%s 帳戶%s 金額%s 地點%s 每月%s號 備註:%s" %(dictRow['IE'], dictRow['name'], dictRow['category'], dictRow['account'], dictRow['amount'], dictRow['location'], dictRow['day'], dictRow['note']))

    @classmethod
    def update(cls):
        cls.hint_select_update_name()
        name = input()
        query = cls.table.select().where(cls.table.c.name == name)
        result = cls.conn.execute(query)
        rows = result.fetchall()
        if len(rows) == 0:
            print("未找到名稱為 \"%s\" 的固定收支" % name)
            return False
        else:
            cls.hint_update_option()
            while True:
                try:
                    option = FixedIEUpdateOption(int(input()))
                    break
                except ValueError:
                    print("請輸入 1 到 7 之間的數字:",)

            if option == FixedIEUpdateOption.CATEGORY:
                return cls.update_category(name)
            elif option == FixedIEUpdateOption.ACCOUNT:
                return cls.update_account(name)
            elif option == FixedIEUpdateOption.AMOUNT:
                return cls.update_amount(name)
            elif option == FixedIEUpdateOption.LOCATION:
                return cls.update_location(name)
            elif option == FixedIEUpdateOption.DAY:
                return cls.update_day(name)
            elif option == FixedIEUpdateOption.NOTE:
                return cls.update_note(name)
            else:
                return True

    @staticmethod
    def hint_select_update_name():
        print("請輸入要修改的固定收支的名稱:")

    @staticmethod
    def hint_update_option():
        print("請選擇要修改的項目(1 類別, 2 帳戶, 3 金額, 4 地點, 5 時間, 6 備註, 7 返回):")

    @classmethod
    def update_category(cls, name):
        new_category = cls.askCategory()
        query = cls.table.update().where(cls.table.c.name == name).values(category=new_category)
        rowsAffected = cls.conn.execute(query).rowcount
        successful = (rowsAffected == 1)
        if not successful:
            return False
        else:
            print("名稱為 \"%s\" 的固定收支類別已成功更新為 %s" % (name, new_category))
            return True

    @staticmethod
    def hintGetCategory():
        print("請輸入紀錄類型:")

    @classmethod
    def update_account(cls, name):
        new_account = cls.askAccount()
        query = cls.table.update().where(cls.table.c.name == name).values(account=new_account['name'])
        rowsAffected = cls.conn.execute(query).rowcount
        successful = (rowsAffected == 1)
        if not successful:
            return False
        else:
            print("名稱為 \"%s\" 的固定收支帳戶已成功更新為 %s" % (name, new_account['name']))
            return True

    @staticmethod
    def hintGetAccount():
        print("請輸入帳戶:")

    @classmethod
    def update_amount(cls, name):
        new_amount = cls.askAmount()
        query = cls.table.update().where(cls.table.c.name == name).values(amount=new_amount)
        rowsAffected = cls.conn.execute(query).rowcount
        successful = (rowsAffected == 1)
        if not successful:
            return False
        else:
            print("名稱為 \"%s\" 的固定收支金額已成功更新為 %.2f" % (name, new_amount))
            return True

    @staticmethod
    def hintGetAmount():
        print("請輸入金額:")

    @classmethod
    def update_location(cls, name):
        new_location = cls.askLocation()
        query = cls.table.update().where(cls.table.c.name == name).values(location=new_location)
        rowsAffected = cls.conn.execute(query).rowcount
        successful = (rowsAffected == 1)
        if not successful:
            return False
        else:
            print("名稱為 \"%s\" 的固定收支地點已成功更新為 %s" % (name, new_location))
            return True

    @staticmethod
    def hintGetLocation():
        print("請輸入地點:")

    @classmethod
    def update_day(cls, name):
        cls.hint_update_day()
        new_day = cls.askDay()
        query = cls.table.update().where(cls.table.c.name == name).values(day=new_day)
        rowsAffected = cls.conn.execute(query).rowcount
        successful = (rowsAffected == 1)
        if not successful:
            return False
        else:
            print("名稱為 \"%s\" 的固定收支時間已成功更新為每月 %d 號" % (name, new_day))
            return True

    @staticmethod
    def hint_update_day():
        print("修改每月收支日為(1-31):")

    @classmethod
    def update_note(cls, name):
        new_note = cls.askNote()
        query = cls.table.update().where(cls.table.c.name == name).values(note=new_note)
        rowsAffected = cls.conn.execute(query).rowcount
        successful = (rowsAffected == 1)
        if not successful:
            return False
        else:
            print("名稱為 \"%s\" 的固定收支備註已成功更新為 %s" % (name, new_note))
            return True

    @staticmethod
    def hintGetNote():
        print("請輸入備註:")

    @classmethod
    def delete(cls):
        cls.hint_delete_name()
        name = input()
        query = cls.table.delete().where(cls.table.c.name == name)
        rowsAffected = cls.conn.execute(query).rowcount
        if rowsAffected == 0:
            print("未找到名稱為 \"%s\" 的固定收支" % name)
            return False
        else:
            print("名稱為 \"%s\" 的固定收支已成功刪除" % name)
            return True

    @staticmethod
    def hint_delete_name():
        print("請輸入要刪除的固定收支的名稱:")

    @classmethod
    def start(cls):
        while True:
            cls.show()
            option = cls.choose()
            if option is FixedIEOption.BACK:
                return
            cls.execute(option)
