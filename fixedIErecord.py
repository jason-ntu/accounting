from enum import IntEnum, auto
import sqlalchemy as sql
import mysqlConfig as cfg
import const
from datetime import datetime
from fixedIE import FixedIEPage, FixedIEType, CategoryOption, PaymentOption

class fixedIERecord():

    @classmethod
    def readFixedIE(cls):

        table_name = "FixedIE"

        cls.setUp_connection_and_table(table_name)
        query = sql.select(cls.table.c['IE', 'name', 'category', 'payment', 'amount', 'day', 'note'])
        results = cls.conn.execute(query).fetchall()
        FixedIEPage.format_print(results)
        cls.conn.commit()
        cls.conn.close()
        return results

    @classmethod
    def newFixedIERocord(cls, dictRow):
        table_name = "Record"

        spendingTime = datetime.now().date()
        deducteTime = datetime.now().date()
        """
        cls.setUp_connection_and_table(table_name)
        query = cls.table.insert().values(IE = dictRow['IE'].name,
                                          category = dictRow['category'].name,
                                          payment = dictRow['payment'].name,
                                          amount = dictRow['amount'],
                                          location = 'none',
                                          consumptionDate = datetime.now().date(),
                                          deductionDate = datetime.now().date(),
                                          invoice = '',
                                          note = dictRow['note'])
        resultProxy = cls.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        successful = (resultProxy.rowcount == 1)
        if not successful:
            print("新增資料失敗")
            cls.conn.rollback()
        else:
            print("新增資料成功")
            cls.conn.commit()
        cls.conn.close()
        """

    @classmethod
    def start(cls):
        results = cls.readFixedIE()
        for row in results:
            dictRow = row._asdict()
            if datetime.now().date().day == dictRow['day'] :
                cls.newFixedIERocord(dictRow)

    @classmethod
    def setUp_connection_and_table(cls, table_name):
        engine = sql.create_engine(cfg.dev['url'])
        cls.conn = engine.connect()
        metadata = sql.MetaData()
        cls.table = sql.Table(table_name, metadata,
                              mysql_autoload=True, autoload_with=engine)


if __name__ == "__main__":  # pragma: no cover
    fixedIERecord = fixedIERecord
    fixedIERecord.start()