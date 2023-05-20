import io
from unittest import TestCase
from unittest.mock import patch
from createRecord import CreateRecordPage, CreateRecordOption, PaymentOption
from mock_db import MockDB
from accessor import ExecutionStatus as es
import const
from datetime import datetime

class TestCreateRecord(MockDB):
    
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_show(self, _stdout):
        CreateRecordPage.show()
        output_lines = _stdout.getvalue().strip().split("\n")
        self.assertEqual(output_lines[0], "%d: 新增食物類別" % CreateRecordOption.FOOD)
        self.assertEqual(output_lines[1], "%d: 新增飲料類別" % CreateRecordOption.BEVERAGE)
        self.assertEqual(output_lines[2], "%d: 回到上一頁" % CreateRecordOption.BACK)
    
    

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["0", "6", "F", "1", "2", "3"])
    def test_choose(self, _input, _stdout):
        self.assertEqual(CreateRecordPage.choose(), 1)
        self.assertEqual(_input.call_count, 4)
        self.assertEqual(CreateRecordPage.choose(), 2)
        self.assertEqual(_input.call_count, 5)
        self.assertEqual(CreateRecordPage.choose(), 3)
        self.assertEqual(_input.call_count, 6)
        self.assertEqual(_stdout.getvalue(), "請輸入 1 到 3 之間的數字:\n" * 3)

    
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['0', 'T', '1', '2', '3', '4', '5'])
    def test_choosePayment(self, _input,  _stdout):
        self.assertEqual(CreateRecordPage.choosePayment(), "CASH")
        self.assertEqual(_input.call_count, 3)
        self.assertEqual(CreateRecordPage.choosePayment(), "DEBIT_CARD")
        self.assertEqual(_input.call_count, 4)
        self.assertEqual(CreateRecordPage.choosePayment(), "CREDIT_CARD")
        self.assertEqual(_input.call_count, 5)
        self.assertEqual(CreateRecordPage.choosePayment(), "ELECTRONIC")
        self.assertEqual(_input.call_count, 6)
        self.assertEqual(CreateRecordPage.choosePayment(), "OTHER")
        self.assertEqual(_input.call_count, 7)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "支付方式 1 現金 2 借記卡 3 信用卡 4 電子支付 5 其他: ")
        self.assertEqual(output_lines[1], "請輸入 1 到 5 之間的數字:")
        self.assertEqual(output_lines[2], "支付方式 1 現金 2 借記卡 3 信用卡 4 電子支付 5 其他: ")

    
    @patch.object(CreateRecordPage, "createRecord")
    def test_execute(self, _createRecord):
        CreateRecordPage.execute(CreateRecordOption.FOOD)
        self.assertEqual(_createRecord.call_count, 1)
        CreateRecordPage.execute(CreateRecordOption.BEVERAGE)
        self.assertEqual(_createRecord.call_count, 2)


    # 除了read之外如何確定有真的insert？
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=[8, 1, 100, "全家", '2023-05-21'])
    @patch.object(CreateRecordPage, "hintPaymentMsg")
    @patch.object(CreateRecordPage, "hintGetAmount")
    @patch.object(CreateRecordPage, "hintGetPlace")
    @patch.object(CreateRecordPage, "hintGetTime")
    def test_createRecord(self, _hintGetTime, _hintGetPlace, _hintGetAmount, _hintPaymentMsg, _input, _stdout):
        with self.mock_db_config:
            CreateRecordPage.setUp_connection_and_table()
            CreateRecordPage.createRecord()
            CreateRecordPage.tearDown_connection(es.NONE)
        self.assertEqual(_hintPaymentMsg.call_count, 2)
        self.assertEqual(_hintGetAmount.call_count, 1)
        self.assertEqual(_hintGetPlace.call_count, 1)
        self.assertEqual(_hintGetTime.call_count, 1)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "請輸入 1 到 5 之間的數字:")

    
    @patch.object(CreateRecordPage, "execute")
    @patch.object(CreateRecordPage, "choose",
        side_effect=[CreateRecordOption.FOOD, CreateRecordOption.BEVERAGE, CreateRecordOption.BACK],
    )
    @patch.object(CreateRecordPage, "show")
    def test_start(self, _show, _choose, _execute):
        CreateRecordPage.start()
        self.assertEqual(_show.call_count, 3)
        self.assertEqual(_choose.call_count, 3)
        self.assertEqual(_execute.call_count, 2)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_hints(self, _stdout):
        hints = [(CreateRecordPage.hintGetAmount, "請輸入金額\n"),
                 (CreateRecordPage.hintGetPlace, "請輸入消費地點\n"),
                 (CreateRecordPage.hintGetTime, "請輸入消費時間(yyyy-mm-dd)\n"),
                 (CreateRecordPage.hintIntegerErorMsg, "輸入的數字須為整數\n"),
                 (CreateRecordPage.hintPaymentMsg, "支付方式 1 現金 2 借記卡 3 信用卡 4 電子支付 5 其他: \n")]
        
        for hint in hints:
            hint[0]()
            self.assertMultiLineEqual(_stdout.getvalue(), hint[1])
            _stdout.truncate(0)
            _stdout.seek(0)