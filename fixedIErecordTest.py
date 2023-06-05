import io
from unittest.mock import patch
import sqlalchemy as sql
from mock_db import MockDB
from accessor import ExecutionStatus as es
from fixedIErecord import fixedIERecord
from datetime import datetime, date
from freezegun import freeze_time

class TestExportPage(MockDB):

    def test_readFixedIE(self):
        with self.mock_db_config:
            fixedIERecord.setUp_connection_and_table(["FixedIE"])
            results = fixedIERecord.readFixedIE()
            fixedIERecord.tearDown_connection(es.NONE)

        fixedIE = [('INCOME', '薪水', '其他', '中華郵政', 48000.0, '其它', 4, '', datetime(2023, 5, 18, 0, 0), 0),
                   ('INCOME', '獎學金', '獎金', '中華郵政', 10000.0, '其它', 18, '', datetime(2023, 5, 18, 0, 0), 0),
                   ('EXPENSE', '房租', '其它', '其它', 6000.0, '其它', 31, 'sos', datetime(2023, 5, 18, 0, 0), 0)]
        self.assertEqual(fixedIE, results)

    def test_newFixedIERocord(self):
        fixedIE = {'IE': 'EXPENSE', 'name': 'YOUTUBE premium', 'category': '其它', 'account': 'Line Pay', 'amount': 50.0, 'location': '其它', 'day': 6, 'note': 'youtube premium', 'registerTime': datetime(2023, 5, 3, 0, 0), 'flag': 0}
        with self.mock_db_config:
            fixedIERecord.newFixedIERocord(fixedIE, "2023-05-06")
        with self.mock_db_config:
            fixedIERecord.setUp_connection_and_table(["Record"])
            query = sql.select(fixedIERecord.tables[0].c["IE", "category", "account", "amount", "location", "purchaseDate", "debitDate", "invoice", "note"]).where(fixedIERecord.tables[0].c.id == 9)
            result = fixedIERecord.conn.execute(query).fetchone()
            fixedIERecord.tearDown_connection(es.NONE)
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
        self.assertEqual(record_dict, result._asdict())

    def test_getEndTime(self):
        with self.mock_db_config:
            fixedIERecord.setUp_connection_and_table(["EndTime"])
            end_time = fixedIERecord.getEndTime()
            fixedIERecord.tearDown_connection(es.NONE)
        self.assertEqual(end_time.strftime("%Y-%m-%d %H:%M:%S"), "2023-05-04 00:13:45")
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_recordEndTime(self, _stdout):
        with self.mock_db_config:
            fixedIERecord.setUp_connection_and_table(["EndTime"])
            end_time = datetime.today().replace(microsecond=0)
            fixedIERecord.recordEndTime(end_time)
            fixedIERecord.tearDown_connection(es.NONE)

        with self.mock_db_config:
            fixedIERecord.setUp_connection_and_table(["EndTime"])
            query = sql.select(fixedIERecord.tables[0].c.time)
            result = fixedIERecord.conn.execute(query).fetchone()
            fixedIERecord.tearDown_connection(es.NONE)

        dictRow = result._asdict()
        self.assertEqual(dictRow['time'], end_time)

    def test_updateFlag(self):
        with self.mock_db_config:
            fixedIERecord.setUp_connection_and_table(["FixedIE"])
            fixedIERecord.updateFlag("獎學金", False)
            fixedIERecord.updateFlag("fake", False)
            fixedIERecord.tearDown_connection(es.NONE)

        with self.mock_db_config:
            fixedIERecord.setUp_connection_and_table(["FixedIE"])
            query = sql.select(fixedIERecord.tables[0].c["name", "flag"]).where(fixedIERecord.tables[0].c.name == "獎學金")
            results = fixedIERecord.conn.execute(query).fetchall()
            fixedIERecord.tearDown_connection(es.NONE)

        dictRow = results[0]._asdict()
        self.assertEqual(dictRow['name'],"獎學金")
        self.assertEqual(dictRow['flag'],0)

    @freeze_time("2023-05-18")
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch.object(fixedIERecord, 'recordEndTime')
    @patch.object(fixedIERecord, 'readFixedIE')
    @patch.object(fixedIERecord, 'getEndTime')
    def test_start(self, _getEndTime , _readFixedIE, _recordEndTime, _stdout):
        with self.mock_db_config:
            fixedIERecord.setUp_connection_and_table(["FixedIE"])
            query = sql.select(fixedIERecord.tables[0].c["name", "IE" , "category", "account", "amount", "location", "day", "note", "registerTime", "flag"])
            _readFixedIE.return_value = fixedIERecord.conn.execute(query).fetchall()
            fixedIERecord.tearDown_connection(es.NONE)

            # For logic testing in this function,
            # CC, PC, and CACC are all covered.
            #     C1: dictRow['day'] < dictRow['registerTime'].day
            #     C2: now_time.month == dictRow['registerTime'].month
            #     C3: now_time.year == dictRow['registerTime'].year
            #     P: C1 and C2 and C3

            # case1 - cross year
            # C1: F, C2: T, C3: F, P: F
            _getEndTime.return_value = datetime(2022, 5, 18, 0, 0, 0)
            fixedIERecord.start()

            # case2 - cross month
            # C1: F, C2: F, C3: T, P: F
            _getEndTime.return_value = datetime(2023, 4, 18, 0, 0, 0)
            fixedIERecord.start()

            # case3 - cross day
            # C1: T, C2: T, C3: T, P: T
            _getEndTime.return_value = datetime(2023, 5, 1, 0, 0, 0)
            fixedIERecord.start()

            # case4 - same date
            # C1: F, C2: T, C3: T, P: F
            _getEndTime.return_value = datetime(2023, 5, 18, 0, 0, 0)
            fixedIERecord.start()
            
            # CC of C1: (case1, case3)
            # CC of C2: (case1, case2)
            # CC of C3: (case1, case2)
            # PC: (case1, case3)
            # C1-majored CACC: (case1, case3)
            # C2-majored CACC: (case2, case3)
            # C3-majored CACC: (case1, case3)

        self.assertEqual(_getEndTime.call_count, 4)
        self.assertEqual(_readFixedIE.call_count, 4)
        self.assertEqual(_recordEndTime.call_count, 4)
        #self.assertEqual(_stdout.getvalue(), "自動記錄固定收支...\n" * 3)




