import sqlalchemy as sql
import mysqlConfig as cfg

class Accessor:

    table_name = ""

    @classmethod
    def setUp_connection_and_table(cls):
        engine = sql.create_engine(cfg.dev['url'])
        cls.conn = engine.connect()
        metadata = sql.MetaData()
        cls.table = sql.Table(cls.table_name, metadata,
                              mysql_autoload=True, autoload_with=engine)

    @classmethod
    def tearDown_connection(cls):
        cls.conn.commit()
        cls.conn.close()
