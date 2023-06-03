import io
from unittest import TestCase
from unittest.mock import patch
from invoice import InvoicePage, InvoiceOption, InvoiceText
from mock_db import MockDB
from datetime import datetime
from freezegun import freeze_time
from accessor import ExecutionStatus as es
from datetime import date
from unittest.mock import Mock

class TestInvoicePage(MockDB):
# [(1, 'INCOME', '薪資', '錢包', 11.0, '餐廳', datetime.date(2023, 1, 30), datetime.date(2023, 1, 30), '12322152', '2434324'), (2, 'EXPENSE', '食物', '儲蓄卡', 23.0, '餐廳', datetime.date(2023, 2, 22), datetime.date(2023, 2, 22), '66882140', '323')]
# self.dicLatest = {'period': '112年01-02月中獎號碼單', 'award1': '06634385', 'award2': '66882140', 'award3': ['25722152', '93412693', '16957025']}
    records = []
    dicLatest = {}

    def setUp(self):
        self.invoicePage = InvoicePage()
        self.dicLatest = {'period': '112年01-02月中獎號碼單', 'award1': '06634385', 'award2': '66882140', 'award3': ['25722152', '93412693', '16957025']}
        self.records = [(7, 'EXPENSE', '衣服', 'LinePay', 321.0, '百貨公司', date.fromisoformat('2023-03-05'), date.fromisoformat('2023-03-05'), '', '洋裝'), (8, 'EXPENSE', '食物', '信用卡', 70.0, '百貨公司', date.fromisoformat('2023-03-28'), date.fromisoformat('2023-03-30'), '', 'coco')]

    @patch.object(InvoicePage, 'choose', side_effect = [InvoiceOption.BACK])
    @patch.object(InvoicePage, 'show')
    @patch.object(InvoicePage, 'goPair')
    @patch.object(InvoicePage, 'queryLatest')
    def test_start_Y(self, m_queryLatest, m_goPair, m_show, m_choose):
        # spy
        def fake_queryLatest_Y():
            self.invoicePage.dicLatest = self.dicLatest


        m_queryLatest.side_effect = fake_queryLatest_Y
        self.invoicePage.start()
        self.assertEqual(m_queryLatest.call_count, 1)
        self.assertEqual(m_goPair.call_count, 1)
        self.assertEqual(m_show.call_count, 1)
        self.assertEqual(m_choose.call_count, 1)

    @patch("sys.stdout", new_callable = io.StringIO)
    @patch.object(InvoicePage, 'choose', side_effect = [InvoiceOption.BACK])
    @patch.object(InvoicePage, 'show')
    @patch.object(InvoicePage, 'goPair')
    @patch.object(InvoicePage, 'queryLatest')
    def test_start_N(self, m_queryLatest, m_goPair, m_show, m_choose, m_stdout):
        # spy
        def fake_queryLatest_N():
            self.invoicePage.dicLatest = {}


        m_queryLatest.side_effect = fake_queryLatest_N
        self.invoicePage.start()
        outputLines = m_stdout.getvalue().strip().split('\n')
        self.assertEqual(m_queryLatest.call_count, 1)
        self.assertEqual(m_goPair.call_count, 0)
        self.assertEqual(m_show.call_count, 1)
        self.assertEqual(m_choose.call_count, 1)
        self.assertEqual(outputLines[0], InvoiceText.NODATA)

    @patch("sys.stdout", new_callable = io.StringIO)
    def test_show(self, m_stdout):
        self.invoicePage.show()
        outputLines = m_stdout.getvalue().strip().split('\n')
        self.assertEqual(outputLines[0], str(InvoiceText.TITLE))
        self.assertEqual(outputLines[1], str(InvoiceText.BACK))
        self.assertEqual(outputLines[2], str(InvoiceText.TITLE))

    @patch("builtins.input", side_effect=["7", "1",])
    @patch("sys.stdout", new_callable = io.StringIO)
    def test_choose(self, m_stdout, m_input):
        self.assertEqual(self.invoicePage.choose(), InvoiceOption.BACK)
        self.assertEqual(m_input.call_count, 2)
        self.assertEqual(m_stdout.getvalue(), (InvoiceText.HINT + "\n\n") * 1)

    def test_queryLatest(self):
        self.invoicePage.queryLatest()
        self.assertIn('月中獎號碼單', self.invoicePage.dicLatest["period"])
        self.assertEqual(8, len(self.invoicePage.dicLatest["award1"]))
        self.assertEqual(8, len(self.invoicePage.dicLatest["award2"]))
        self.assertEqual(3, len(self.invoicePage.dicLatest["award3"]))

    def test_queryRecord(self):
        with self.mock_db_config:
            self.invoicePage.setUp_connection_and_table()
            results = self.invoicePage.queryRecord('2023-03-01', '2023-03-31')
            self.invoicePage.tearDown_connection(es.NONE)

        records = [(7, 'EXPENSE', '衣服', 'LinePay', 321.0, '百貨公司', date.fromisoformat('2023-03-05'), date.fromisoformat('2023-03-05'), '', '洋裝'), (8, 'EXPENSE', '食物', '信用卡', 70.0, '百貨公司', date.fromisoformat('2023-03-28'), date.fromisoformat('2023-03-30'), '', 'coco')]
        self.assertEqual(records, results)

    @patch("sys.stdout", new_callable = io.StringIO)
    @patch.object(InvoicePage, 'checkNumbers', side_effect = ['對中 20 萬元！', '對中 20 萬元！', '', ''])
    @patch.object(InvoicePage, 'queryRecord')
    def test_goPair(self, m_queryRecord, m_checkNumbers, m_stdout):
        self.invoicePage.dicLatest = self.dicLatest
        
        #有record有中獎
        m_queryRecord.return_value = self.records
        self.invoicePage.goPair()

        #有record沒中獎
        m_queryRecord.return_value = self.records
        self.invoicePage.goPair()

        #沒record
        m_queryRecord.return_value = []
        self.invoicePage.goPair()

        outputLines = m_stdout.getvalue().strip().split('\n')
        self.assertIn('月中獎號碼單', outputLines[0])
        self.assertEqual(InvoiceText.NOPAIR, outputLines[9])
        self.assertEqual(InvoiceText.NOPAIR, outputLines[11])
        self.assertEqual(m_queryRecord.call_count, 3)
        self.assertEqual(m_checkNumbers.call_count, 4)

    def test_checkNumbers(self):
        self.invoicePage.dicLatest = self.dicLatest
        self.assertEqual(self.invoicePage.checkNumbers('06634385'), '對中 1000 萬元！')
        self.assertEqual(self.invoicePage.checkNumbers('66882140'), '對中 200 萬元！')
        self.assertEqual(self.invoicePage.checkNumbers('93412693'), '對中 20 萬元！')
        self.assertEqual(self.invoicePage.checkNumbers('03412693'), '對中 4 萬元！')
        self.assertEqual(self.invoicePage.checkNumbers('00412693'), '對中 1 萬元！')
        self.assertEqual(self.invoicePage.checkNumbers('00012693'), '對中 4000 元！')
        self.assertEqual(self.invoicePage.checkNumbers('00002693'), '對中 1000 元！')
        self.assertEqual(self.invoicePage.checkNumbers('00000693'), '對中 200 元！')
