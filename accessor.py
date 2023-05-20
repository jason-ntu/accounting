from enum import IntEnum, auto
import sqlalchemy as sql
import mysqlConfig as cfg
import const

class ExecutionStatus(IntEnum):
    NONE = auto()
    COMMIT = auto()
    ROLLBACK = auto()

class Accessor:

    table_name = ""

    @classmethod
    def setUp_connection_and_table(cls, tables=[]):
        engine = sql.create_engine(cfg.dev['url'])
        cls.conn = engine.connect()
        metadata = sql.MetaData()
        # use cls.table to access the default table
        if len(tables) == 0:
            cls.table = sql.Table(cls.table_name, metadata,
                              mysql_autoload=True, autoload_with=engine)
            return
        # use cls.tables to access user-defined tables
        cls.tables = []
        for table in tables:
            cls.tables.append(sql.Table(table, metadata,
                            mysql_autoload=True, autoload_with=engine))


    @classmethod
    def tearDown_connection(cls, operation=ExecutionStatus.COMMIT):
        if operation is ExecutionStatus.COMMIT:
            cls.conn.commit()
            print("%s操作成功%s" % (const.ANSI_GREEN, const.ANSI_RESET))
        elif operation is ExecutionStatus.ROLLBACK:
            cls.conn.rollback()
            print("%s操作失敗%s" % (const.ANSI_RED, const.ANSI_RESET))
        else:
            pass
        cls.conn.close()
