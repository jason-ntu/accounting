from enum import IntEnum, auto
import sqlalchemy as sql
from accessor import Accessor, ExecutionStatus as es
from recordDirection import RecordDirection, askIE
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
    def show(IE):
        IEtext = "收入"
        if IE == RecordDirection.EXPENSE:
            IEtext = "支出"
        print(f"{CategoryOption.CREATE}: 新增{IEtext}類別")
        print(f"{CategoryOption.READ}: 查看{IEtext}類別")
        print(f"{CategoryOption.UPDATE}: 修改{IEtext}類別")
        print(f"{CategoryOption.DELETE}: 刪除{IEtext}類別")
        print(f"{CategoryOption.BACK}: 回到上一頁")

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
    def execute(cls, IE, option):
        cls.setUp_connection_and_table()
        if option is CategoryOption.CREATE:
            successful = cls.create(IE)
        elif option is CategoryOption.READ:
            cls.read(IE)
            cls.tearDown_connection(es.NONE)
            return
        elif option is CategoryOption.UPDATE:
            successful = cls.update(IE)
        else:
            successful = cls.delete(IE)
        if successful:
            cls.tearDown_connection(es.COMMIT)
        else:
            cls.tearDown_connection(es.ROLLBACK)

    @classmethod
    def create(cls, IE):
        cls.hint_create_name()
        name = input()
        if name == "":
            print("%s名稱不得為空%s" % (const.ANSI_YELLOW, const.ANSI_RESET))
            return False
        query = sql.select(cls.table.c["name"]).where(sql.and_(cls.table.c.name == name,cls.table.c.IE == IE.name))
        results = cls.conn.execute(query).fetchall()
        if len(results) > 0:
            print("%s名稱不得與既有類別的名稱重複%s" % (const.ANSI_YELLOW, const.ANSI_RESET))
            return False
        query = cls.table.insert().values(name=name, IE=IE.name)
        rowsAffected = cls.conn.execute(query).rowcount
        return rowsAffected == 1

    @staticmethod
    def hint_create_name():
        print("請輸入新類別的名稱:")

    @classmethod
    def read(cls, IE):
        query = sql.select(cls.table.c["name", "IE"]).where(cls.table.c.IE == IE.name)
        results = cls.conn.execute(query).fetchall()
        for row in results:
            dictRow = row._asdict()
            print(dictRow['name'])

    @classmethod
    def update(cls, IE):
        cls.hint_update_name()
        name = input()
        cls.hint_update_new_name()
        new_name = input()
        if new_name == "":
            print("%s新名稱不得為空%s" % (const.ANSI_YELLOW, const.ANSI_RESET))
            return False
        query = sql.select(cls.table.c["name"]).where(sql.and_(cls.table.c.name == new_name, cls.table.c.IE == IE.name))
        results = cls.conn.execute(query).fetchall()
        # TODO: CACC Jason
        if len(results) > 0 and name != new_name:
            print("%s新名稱不得與既有類別的名稱重複%s" %
                  (const.ANSI_YELLOW, const.ANSI_RESET))
            return False

        query = cls.table.update().values(name=new_name).where(sql.and_(cls.table.c.name == name, cls.table.c.IE == IE.name))
        rowsAffected = cls.conn.execute(query).rowcount
        if rowsAffected == 0:
            print("%s目前沒有這個類別%s" %
                  (const.ANSI_YELLOW, const.ANSI_RESET))
            return False
        return True

    @staticmethod
    def hint_update_name():
        print("請輸入要修改的類別名稱:")

    @staticmethod
    def hint_update_new_name():
        print("請輸入新的名稱:")

    @classmethod
    def delete(cls, IE):
        cls.hint_delete()
        name = input()
        if name == "":
            print("%s名稱不得為空%s" % (const.ANSI_YELLOW, const.ANSI_RESET))
            return False
        query = cls.table.delete().where(sql.and_(cls.table.c.name == name, cls.table.c.IE == IE.name))
        rowsAffected = cls.conn.execute(query).rowcount
        if rowsAffected == 0:
            print("%s目前沒有這個類別%s" %
                  (const.ANSI_YELLOW, const.ANSI_RESET))
            return False
        return True

    @staticmethod
    def hint_delete():
        print("請輸入要刪除的類別名稱:")

    @classmethod
    def start(cls):
        while True:
            cls.hint_IE()
            IE = askIE()
            cls.show(IE)
            option = cls.choose()
            if option is CategoryOption.BACK:
                return
            cls.execute(IE, option)
    
    @staticmethod
    def hint_IE():
        print("請問要操作收入類別還是支出類別:")
    
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