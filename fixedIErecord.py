from enum import IntEnum, auto
import sqlalchemy as sql
import mysqlConfig as cfg
import const
from accessor import Accessor, ExecutionStatus as es
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

class fixedIERecord(Accessor):

    @classmethod
    def readFixedIE(cls):
        cls.setUp_connection_and_table(["FixedIE"])
        query = sql.select(cls.tables[0].c['IE', 'name', 'category', 'account', 'amount', 'location' ,'day', 'note', 'registerTime', 'flag'])
        results = cls.conn.execute(query).fetchall()
        cls.tearDown_connection(es.NONE)
        return results

    @classmethod
    def newFixedIERocord(cls, dictRow, date):
        cls.setUp_connection_and_table(["Record"])
        query = cls.tables[0].insert().values(IE = dictRow['IE'],
                                              category = dictRow['category'],
                                              account = dictRow['account'],
                                              amount = dictRow['amount'],
                                              location = dictRow['location'],
                                              purchaseDate = date,
                                              debitDate = date,
                                              invoice = '',
                                              note = dictRow['note'])
        resultProxy = cls.conn.execute(query)
        successful = (resultProxy.rowcount == 1)
        cls.tearDown_connection(es.COMMIT)

    @classmethod
    def getEndTime(cls):
        cls.setUp_connection_and_table(["EndTime"])
        query = sql.select(cls.tables[0].c.time)
        result = cls.conn.execute(query).fetchall()

        time = result[0][0]
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
        cls.tearDown_connection(es.NONE)
        return parse(formatted_time)

    @classmethod
    def recordEndTime(cls ,end_time):
        cls.setUp_connection_and_table(["EndTime"])
        query = sql.select(cls.tables[0]).limit(1)
        result = cls.conn.execute(query).fetchone()

        existing_id = result[0]
        update_query = cls.tables[0].update().where(cls.tables[0].c.id == existing_id).values(time=end_time)
        cls.conn.execute(update_query)

        cls.tearDown_connection(es.COMMIT)

    @classmethod
    def updateFlag(cls, name, flag):
        cls.setUp_connection_and_table(["FixedIE"])
        query = cls.tables[0].update().where(cls.tables[0].c.name == name).values(flag=flag)
        rowsAffected = cls.conn.execute(query).rowcount
        successful = (rowsAffected == 1)
        if not successful:
            cls.tearDown_connection(es.ROLLBACK)
            return
        cls.tearDown_connection(es.COMMIT)

    @classmethod
    def start(cls):
        last_end_time = cls.getEndTime()
        now_time = datetime.today()

        results = cls.readFixedIE()
        print("自動記錄固定收支...")

        month_difference = now_time.month - last_end_time.month

        for row in results:
            dictRow = row._asdict()

            for m in range(month_difference, -1, -1):
                # TODO: CACC sylvia
                if m == 0 and month_difference > 0:
                    cls.updateFlag(dictRow['name'], False)
                    now_flag = False
                # TODO: CACC yyyenn
                elif dictRow['day'] < dictRow['registerTime'].day and now_time.month == dictRow['registerTime'].month and now_time.year == dictRow['registerTime'].year:
                    cls.updateFlag(dictRow['name'], True)
                    now_flag = True
                else:
                    now_flag = dictRow['flag']

                # TODO: CACC yyyenn
                if now_time.day >= dictRow['day'] and m == 0 and now_flag == False:
                    try:
                        record_date = date(now_time.year, now_time.month, int(dictRow['day']))
                    except ValueError:
                        record_date = None
                    if record_date:
                        cls.newFixedIERocord(dictRow, record_date)
                    cls.updateFlag(dictRow['name'], True)
                    now_flag = True
                # TODO: CACC sylvia
                elif m == 1 and now_flag == True:
                    continue
                elif m > 0:
                    try:
                        record_date = date(now_time.year, now_time.month - m, int(dictRow['day']))
                    except ValueError:
                        record_date = None
                    if record_date:
                        cls.newFixedIERocord(dictRow, record_date)

        cls.recordEndTime(datetime.today())

if __name__ == "__main__":  # pragma: no cover
    fixedIERecord = fixedIERecord
    fixedIERecord.start()