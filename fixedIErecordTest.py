import io
from unittest.mock import patch
import sqlalchemy as sql
from export import ExportPage, ExportOption
from mock_db import MockDB
from accessor import ExecutionStatus as es
from accessor import Accessor
import const
from fixedIErecord import fixedIERecord
from datetime import datetime, date

class TestExportPage(MockDB):

    def test_readFixedIE(self):
        with self.mock_db_config:
            fixedIERecord.setUp_connection_and_table(["FixedIE"])
            results = fixedIERecord.readFixedIE()
            fixedIERecord.tearDown_connection(es.NONE)

        fixedIE = [('INCOME', '獎學金', '獎金', '中華郵政', 10000.0, '其它', 15, '', datetime(2023, 5, 1, 10, 0, 25), 1),
                  ('EXPENSE', '房租', '其它', '其它', 6000.0, '其它', 20, 'sos', datetime(2023, 5, 18, 0, 0), 0)]

        for i, row in enumerate(results):
            fixedIE_dict = {
                'IE': fixedIE[i][0],
                'name': fixedIE[i][1],
                'category': fixedIE[i][2],
                'account': fixedIE[i][3],
                'amount': fixedIE[i][4],
                'location': fixedIE[i][5],
                'day': fixedIE[i][6],
                'note': fixedIE[i][7],
                'registerTime': fixedIE[i][8],
                'flag': fixedIE[i][9]
            }
            dictRow = row._asdict()
            self.assertEqual(fixedIE_dict, dictRow)

    def test_newFixedIERocord(self):
        fixedIE = {'IE': 'EXPENSE', 'name': 'YOUTUBE premium', 'category': '其它', 'account': 'Line Pay', 'amount': 50.0, 'location': '其它', 'day': 6, 'note': 'youtube premium', 'registerTime': datetime(2023, 5, 3, 0, 0), 'flag': 0}
        with self.mock_db_config:
            fixedIERecord.setUp_connection_and_table(["Record"])
            fixedIERecord.newFixedIERocord(fixedIE, "2023-05-06")
            fixedIERecord.tearDown_connection(es.NONE)
        with self.mock_db_config:
            fixedIERecord.setUp_connection_and_table(["Record"])
            query = sql.select(
                        fixedIERecord.tables[0].c.IE,
                        fixedIERecord.tables[0].c.category,
                        fixedIERecord.tables[0].c.account,
                        fixedIERecord.tables[0].c.amount,
                        fixedIERecord.tables[0].c.location,
                        fixedIERecord.tables[0].c.purchaseDate,
                        fixedIERecord.tables[0].c.debitDate,
                        fixedIERecord.tables[0].c.invoice,
                        fixedIERecord.tables[0].c.note,
                    ).where(fixedIERecord.tables[0].c.id == 9)
            results = fixedIERecord.conn.execute(query).fetchall()
            fixedIERecord.tearDown_connection(es.NONE)
        record = ('EXPENSE', '', 'youtube premium')
        record_dict = {
                'IE': 'EXPENSE',
                'category': '其它',
                'account': 'Line Pay',
                'amount': 50.0,
                'location': '其它',
                'purchaseDate': date(2023, 5, 6),
                'debitDate': date(2023, 5, 6),
                'invoice' : '',
                'note': 'youtube premium'
            }
        self.assertEqual(record_dict, results[0]._asdict())

    def test_getEndTime(self):
        with self.mock_db_config:
            fixedIERecord.setUp_connection_and_table(["EndTime"])
            end_time = fixedIERecord.getEndTime()
            fixedIERecord.tearDown_connection(es.NONE)
        self.assertEqual(end_time.strftime("%Y-%m-%d %H:%M:%S"), "2023-05-04 00:13:45")

    def test_recordEndTime(self):
        with self.mock_db_config:
            fixedIERecord.setUp_connection_and_table(["EndTime"])
            end_time = datetime.today().replace(microsecond=0)
            fixedIERecord.recordEndTime(end_time)
            fixedIERecord.tearDown_connection(es.NONE)

        with self.mock_db_config:
            fixedIERecord.setUp_connection_and_table(["EndTime"])
            query = sql.select(fixedIERecord.tables[0].c.time)
            results = fixedIERecord.conn.execute(query).fetchall()
            fixedIERecord.tearDown_connection(es.NONE)

        dictRow = results[0]._asdict()
        self.assertEqual(dictRow['time'], end_time)

    def test_updateFlag(self):
        with self.mock_db_config:
            fixedIERecord.setUp_connection_and_table(["FixedIE"])
            fixedIERecord.updateFlag("獎學金", False)
            fixedIERecord.tearDown_connection(es.NONE)

        with self.mock_db_config:
            fixedIERecord.setUp_connection_and_table(["FixedIE"])
            query = sql.select(
                        fixedIERecord.tables[0].c.name,
                        fixedIERecord.tables[0].c.flag
                    ).where(fixedIERecord.tables[0].c.name == "獎學金")
            results = fixedIERecord.conn.execute(query).fetchall()
            fixedIERecord.tearDown_connection(es.NONE)

        dictRow = results[0]._asdict()
        self.assertEqual(dictRow['name'],"獎學金")
        self.assertEqual(dictRow['flag'],0)

    # TODO
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(fixedIERecord, 'getEndTime')
    @patch.object(fixedIERecord, 'readFixedIE')
    @patch.object(fixedIERecord, 'recordEndTime')
    def test_start(self, _recordEndTime, _readFixedIE, _getEndTime  ,_stdout):
        fixedIERecord.start()
        self.assertEqual(_recordEndTime.call_count, 1)
        self.assertEqual(_readFixedIE.call_count, 1)
        self.assertEqual(_getEndTime.call_count, 1)
