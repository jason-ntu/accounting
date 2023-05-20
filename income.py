from enum import IntEnum, auto
import sqlalchemy as sql
from accessor import Accessor, ExecutionStatus as es
import const

class IncomeOption(IntEnum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()
    BACK = auto()

class IncomePage(Accessor):

    table_name = "Income"

    @staticmethod
    def show():
        print("[收入設定]")
        print("%d: 新增收入方式" % IncomeOption.CREATE)
        print("%d: 查看收入方式" % IncomeOption.READ)
        print("%d: 修改收入方式" % IncomeOption.UPDATE)
        print("%d: 刪除收入方式" % IncomeOption.DELETE)
        print("%d: 回到上一頁" % IncomeOption.BACK)

    @staticmethod
    def choose():
        while True:
            try:
                option = IncomeOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 5 之間的數字:")
        return option

    @classmethod
    def execute(cls, option):
        cls.setUp_connection_and_table()
        if option is IncomeOption.CREATE:
            successful = cls.create()
        elif option is IncomeOption.READ:
            cls.read()
            cls.tearDown_connection(es.NONE)
            return
        elif option is IncomeOption.UPDATE:
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
        cls.hint_create_name()
        name = input()

        if not name.strip():
            print("%s名稱不得為空%s" % (const.ANSI_YELLOW, const.ANSI_RESET))
            return False

        select_query = cls.table.select().where(cls.table.c.name == name)
        existing_row = cls.conn.execute(select_query).fetchone()
        if existing_row:
            print("%s新名稱不得與其他收入的名稱重複%s" % (const.ANSI_YELLOW, const.ANSI_RESET))
            return False

        query = cls.table.insert().values(name=name)
        rowsAffected = cls.conn.execute(query).rowcount
        return rowsAffected == 1

    @staticmethod
    def hint_create_name():
        print("請輸入新收入方式的...")
        print("名稱:")

    @classmethod
    def read(cls):
        query = sql.select(cls.table.c["name"])
        results = cls.conn.execute(query).fetchall()
        for row in results:
            dictRow = row._asdict()
            print("\"%s\"" %(dictRow['name']))

    @classmethod
    def update(cls):
        cls.hint_update_name()
        name = input()
        cls.hint_update_new_name()

        newName = input()

        if not newName.strip():
            print("%s名稱不得為空%s" % (const.ANSI_YELLOW, const.ANSI_RESET))
            return False

        select_query = cls.table.select().where(cls.table.c.name == newName)
        existing_row = cls.conn.execute(select_query).fetchone()
        if existing_row:
            print("%s新名稱不得與其他收入的名稱重複%s" % (const.ANSI_YELLOW, const.ANSI_RESET))
            return False

        query = cls.table.update().values(name=newName).where(cls.table.c.name == name)
        rowsAffected = cls.conn.execute(query).rowcount

        if rowsAffected == 0:
            print("%s%s 對應不到任何收入方式%s" % (const.ANSI_YELLOW, name, const.ANSI_RESET))
            return False
        else:
            return True

    @staticmethod
    def hint_update_name():
        print("請輸入要修改的收入方式名稱:")

    @staticmethod
    def hint_update_new_name():
        print("請輸入新的名稱:")

    @classmethod
    def delete(cls):
        cls.hint_delete()
        name = input()
        query = cls.table.delete().where(cls.table.c.name == name)
        rowsAffected = cls.conn.execute(query).rowcount
        if rowsAffected == 0:
            print("%s%s 對應不到任何收入方式%s" % (const.ANSI_YELLOW, name, const.ANSI_RESET))
            return False
        return True

    def hint_delete():
        print("請輸入要刪除的收入方式名稱:")

    @classmethod
    def start(cls):
        while True:
            cls.show()
            option = cls.choose()
            if option is IncomeOption.BACK:
                return
            cls.execute(option)


if __name__ == "__main__":  # pragma: no cover
    IncomePage.start()
