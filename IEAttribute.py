from enum import IntEnum, auto
import sqlalchemy as sql
from accessor import Accessor, ExecutionStatus as es
from IEDirection import IEDirection
import const

class IEOption(IntEnum):
    INCOME = IEDirection.INCOME
    EXPENSE = IEDirection.EXPENSE
    BACK = auto()

class Operation(IntEnum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()
    BACK = auto()

# this class is intended to be a base class for CategoryPage and LocationPage
class IEAttribute(Accessor):

    attribute_name = "屬性"
    IE_name = "收支"

    @classmethod
    def hintGetOperation(cls):
        print(f"{Operation.CREATE}: 新增{cls.IE_name}{cls.attribute_name}")
        print(f"{Operation.READ}: 查看{cls.IE_name}{cls.attribute_name}")
        print(f"{Operation.UPDATE}: 修改{cls.IE_name}{cls.attribute_name}")
        print(f"{Operation.DELETE}: 刪除{cls.IE_name}{cls.attribute_name}")
        print(f"{Operation.BACK}: 回到上一頁")

    def chooseOperation():
        while True:
            try:
                option = Operation(int(input()))
                break
            except ValueError:
                print(f"請輸入 1 到 {len(Operation)} 之間的數字:")
        return option

    @classmethod
    def execute(cls, option):
        cls.setUp_connection_and_table()
        if option is Operation.CREATE:
            successful = cls.create()
        elif option is Operation.READ:
            cls.read()
            cls.tearDown_connection(es.NONE)
            return
        elif option is Operation.UPDATE:
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
            print(f"{const.ANSI_YELLOW}新{cls.attribute_name}的名稱不得為空{const.ANSI_RESET}")
            return False
        query = sql.select(cls.table.c["name"]).where(sql.and_(cls.table.c.name == name, cls.table.c.IE == cls.IE.name))
        results = cls.conn.execute(query).fetchall()
        if len(results) > 0:
            print(f"{const.ANSI_YELLOW}新{cls.attribute_name}的名稱不得與既有{cls.attribute_name}的名稱重複{const.ANSI_RESET}")
            return False
        query = cls.table.insert().values(name=name, IE=cls.IE.name)
        rowsAffected = cls.conn.execute(query).rowcount
        return rowsAffected == 1

    @classmethod
    def hint_create_name(cls):
        print(f"請輸入新{cls.attribute_name}的名稱:")

    @classmethod
    def read(cls):
        query = sql.select(cls.table.c["name"]).where(cls.table.c.IE == cls.IE.name)
        results = cls.conn.execute(query).fetchall()
        for row in results:
            dictRow = row._asdict()
            print(dictRow['name'])
        
    @classmethod
    def update(cls):
        cls.hint_update_name()
        name = input()
        cls.hint_update_new_name()
        new_name = input()
        if new_name == "":
            print("%s新名稱不得為空%s" % (const.ANSI_YELLOW, const.ANSI_RESET))
            return False
        query = sql.select(cls.table.c["name"]).where(sql.and_(cls.table.c.name == new_name, cls.table.c.IE == cls.IE.name))
        results = cls.conn.execute(query).fetchall()
        # TODO: CACC Jason
        if len(results) > 0 and name != new_name:
            print(f"{const.ANSI_YELLOW}新名稱不得與既有{cls.attribute_name}的名稱重複{const.ANSI_RESET}")
            return False

        query = cls.table.update().values(name=new_name).where(sql.and_(cls.table.c.name == name, cls.table.c.IE == cls.IE.name))
        rowsAffected = cls.conn.execute(query).rowcount
        if rowsAffected == 0:
            print(f"{const.ANSI_YELLOW}目前沒有這個{cls.attribute_name}{const.ANSI_RESET}")
            return False
        return True
    
    @classmethod
    def hint_update_name(cls):
        print(f"請輸入要修改的{cls.attribute_name}名稱:")

    def hint_update_new_name():
        print("請輸入新的名稱:")

    @classmethod
    def delete(cls):
        cls.hint_delete()
        name = input()
        if name == "":
            print("%s名稱不得為空%s" % (const.ANSI_YELLOW, const.ANSI_RESET))
            return False
        query = cls.table.delete().where(sql.and_(cls.table.c.name == name, cls.table.c.IE == cls.IE.name))
        rowsAffected = cls.conn.execute(query).rowcount
        if rowsAffected == 0:
            print(f"{const.ANSI_YELLOW}目前沒有這個{cls.attribute_name}{const.ANSI_RESET}")
            return False
        return True

    @classmethod
    def hint_delete(cls):
        print(f"請輸入要刪除的{cls.attribute_name}名稱:")

    @classmethod
    def hintGetIE(cls):
        print(f"請問要操作收入{cls.attribute_name}還是支出{cls.attribute_name}:")
        print(f"{IEOption.INCOME}: 收入")
        print(f"{IEOption.EXPENSE}: 支出")  
        print(f"{IEOption.BACK}: 回到上一頁")

    def chooseIE():
        while True:
            try:
                IE = IEOption(int(input()))
                break
            except ValueError:
                print(f"請輸入 1 到 {len(IEOption)} 之間的數字:")
        return IE

    @classmethod
    def start(cls):
        while True:
            cls.hintGetIE()
            cls.IE = cls.chooseIE()
            if cls.IE is IEOption.INCOME:
                cls.IE_name = "收入"
            elif cls.IE is IEOption.EXPENSE:
                cls.IE_name = "支出"
            else:
                break
            while True:
                cls.hintGetOperation()
                option = cls.chooseOperation()
                if option is Operation.BACK:
                    break
                cls.execute(option) 

    @classmethod
    def getList(cls, IE):
        cls.setUp_connection_and_table()
        query = sql.select(cls.table.c['name']).where(cls.table.c.IE == IE)
        results = cls.conn.execute(query).fetchall()
        cls.tearDown_connection(es.NONE)
        locationList = []
        for result in results:
            locationList.append(result[0])
        return locationList
