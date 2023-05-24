from enum import IntEnum, auto
import sqlalchemy as sql
from accessor import Accessor, ExecutionStatus as es
import const

class CategoryOption(IntEnum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()
    BACK = auto()


class CategoryPage(Accessor):

    table_name = "Category"
    
    @staticmethod
    def show():
        print("%d: 新增類別" % CategoryOption.CREATE)
        print("%d: 查看類別" % CategoryOption.READ)
        print("%d: 修改類別" % CategoryOption.UPDATE)
        print("%d: 刪除類別" % CategoryOption.DELETE)
        print("%d: 回到上一頁" % CategoryOption.BACK)

    @staticmethod
    def choose():
        while True:
            try:
                option = CategoryOption(int(input()))
                break
            except ValueError:
                print("請輸入 1 到 5 之間的數字:")
        return option

    @classmethod
    def execute(cls, option):
        cls.setUp_connection_and_table()
        if option is CategoryOption.CREATE:
            successful = cls.create()
        elif option is CategoryOption.READ:
            cls.read()
            cls.tearDown_connection(es.NONE)
            return
        elif option is CategoryOption.UPDATE:
            successful = cls.update()
        else:
            successful = cls.delete()
        if successful:
            cls.tearDown_connection(es.COMMIT)
        else:
            cls.tearDown_connection(es.ROLLBACK)

    @classmethod
    def create(cls):
        cls.hint_create_name()
        name = input()
        if name == "":
            print("%s名稱不得為空%s" % (const.ANSI_YELLOW, const.ANSI_RESET))
            return False
        query = sql.select(cls.table.c["name"]).where(cls.table.c.name == name)
        results = cls.conn.execute(query).fetchall()
        if len(results) > 0:
            print("%s名稱不得與其它類別的名稱重複%s" % (const.ANSI_YELLOW, const.ANSI_RESET))
            return False
        query = cls.table.insert().values(name=name)
        rowsAffected = cls.conn.execute(query).rowcount
        return rowsAffected == 1

    @staticmethod
    def hint_create_name():
        print("請輸入新類別的名稱:")

    @classmethod
    def read(cls):
        query = sql.select(cls.table.c["name", "IE"])
        results = cls.conn.execute(query).fetchall()
        for row in results:
            dictRow = row._asdict()
            print(f"{dictRow['name']} {dictRow['IE']}")

    @classmethod
    def update(cls):
        cls.hint_update_name()
        name = input()
        cls.hint_update_new_name()
        new_name = input()
        if new_name == "":
            print("%s新名稱不得為空%s" % (const.ANSI_YELLOW, const.ANSI_RESET))
            return False
        query = sql.select(cls.table.c["name"]).where(
            cls.table.c.name == new_name)
        results = cls.conn.execute(query).fetchall()
        if len(results) > 0 and name != new_name:
            print("%s新名稱不得與其它類別的名稱重複%s" %
                  (const.ANSI_YELLOW, const.ANSI_RESET))
            return False
        query = cls.table.update().values(name=new_name).where(cls.table.c.name == name)
        rowsAffected = cls.conn.execute(query).rowcount
        if rowsAffected == 0:
            print("%s目前沒有這個類別%s" %
                  (const.ANSI_YELLOW, const.ANSI_RESET))
            return False
        return True

    def hint_update_name():
        print("請輸入要修改的類別名稱:")

    def hint_update_new_name():
        print("請輸入新的名稱:")

    @classmethod
    def delete(cls):
        cls.hint_delete()
        name = input()
        if name == "":
            print("%s名稱不得為空%s" % (const.ANSI_YELLOW, const.ANSI_RESET))
            return False
        query = cls.table.delete().where(cls.table.c.name == name)
        rowsAffected = cls.conn.execute(query).rowcount
        if rowsAffected == 0:
            print("%s目前沒有這個類別%s" %
                  (const.ANSI_YELLOW, const.ANSI_RESET))
            return False
        return True

    def hint_delete():
        print("請輸入要刪除的類別名稱:")

    @classmethod
    def start(cls):
        while True:
            cls.show()
            option = cls.choose()
            if option is CategoryOption.BACK:
                return
            cls.execute(option)
    
    @classmethod
    def getList(cls, IE):
        cls.setUp_connection_and_table()
        query = sql.select(cls.table.c['name']).where(cls.table.c.IE == IE)
        results = cls.conn.execute(query).fetchall()
        cls.tearDown_connection(es.NONE)
        categoryList = []
        for result in results:
            categoryList.append(result[0])
        return categoryList

if __name__ == "__main__":  # pragma: no cover
    CategoryPage.start()