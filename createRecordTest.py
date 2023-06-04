import io
from unittest.mock import patch
from createRecord import CreateRecordPage, CreateRecordOption
from mock_db import MockDB
from accessor import ExecutionStatus as es
from datetime import datetime
from records import RecordPage

class TestCreateRecord(MockDB):

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_show(self, _stdout):
        CreateRecordPage.show()
        output_lines = _stdout.getvalue().strip().split("\n")
        self.assertEqual(output_lines[0], "%d: 新增收入" % CreateRecordOption.INCOME)
        self.assertEqual(output_lines[1], "%d: 新增支出" % CreateRecordOption.EXPENSE)
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

    @patch.object(CreateRecordPage, "createRecord")
    def test_execute(self, _createRecord):
        CreateRecordPage.execute(CreateRecordOption.INCOME)
        self.assertEqual(_createRecord.call_count, 1)
        CreateRecordPage.execute(CreateRecordOption.EXPENSE)
        self.assertEqual(_createRecord.call_count, 2)
    
    @patch.object(RecordPage, "updateAccountAmount")
    @patch.object(RecordPage, "askNote", return_value = "")
    @patch.object(RecordPage, "askInvoice", return_value = "")
    @patch.object(RecordPage, "askDebitDate", return_value = datetime.today())
    @patch.object(RecordPage, "askPurchaseDate", return_value = datetime.today())
    @patch.object(RecordPage, "askLocation", return_value = "地點")
    @patch.object(RecordPage, "askAmount", return_value = 100)
    @patch.object(RecordPage, "askAccount", return_value = {'name': '信用卡', 'category': 'CREDIT_CARD'})
    @patch.object(RecordPage, "askCategory", return_value = "類別")
    def test_createRecord(self, _askCategory, _askAccount, _askAmount, _askLocation, _askPurchaseDate, _askDebitDate, _askInvoice, _askNote, _updateAccountAmount):
        with self.mock_db_config:
            CreateRecordPage.IE = 'EXPENSE'
            CreateRecordPage.createRecord()
            CreateRecordPage.tearDown_connection(es.NONE)
        self.assertEqual(_askCategory.call_count, 1)
        self.assertEqual(_askAccount.call_count, 1)
        self.assertEqual(_askAmount.call_count, 1)
        self.assertEqual(_askLocation.call_count, 1)
        self.assertEqual(_askPurchaseDate.call_count, 1)
        self.assertEqual(_askDebitDate.call_count, 1)
        self.assertEqual(_askInvoice.call_count, 1)
        self.assertEqual(_askNote.call_count, 1)
        self.assertEqual(_updateAccountAmount.call_count, 1)
    
    @patch.object(RecordPage, "updateAccountAmount")
    @patch.object(RecordPage, "askNote", return_value = "")
    @patch.object(RecordPage, "askInvoice", return_value = "")
    @patch.object(RecordPage, "askDebitDate", return_value = datetime.today())
    @patch.object(RecordPage, "askPurchaseDate", return_value = datetime.today())
    @patch.object(RecordPage, "askLocation", return_value = "地點")
    @patch.object(RecordPage, "askAmount", return_value = 100)
    @patch.object(RecordPage, "askAccount", return_value = {'name': '現金', 'category': 'CASH'})
    @patch.object(RecordPage, "askCategory", return_value = "類別")
    def test_createRecord2(self, _askCategory, _askAccount, _askAmount, _askLocation, _askPurchaseDate, _askDebitDate, _askInvoice, _askNote, _updateAccountAmount):
        with self.mock_db_config:
            CreateRecordPage.IE = 'EXPENSE'
            CreateRecordPage.createRecord()
            CreateRecordPage.tearDown_connection(es.NONE)
        self.assertEqual(_askCategory.call_count, 1)
        self.assertEqual(_askAccount.call_count, 1)
        self.assertEqual(_askAmount.call_count, 1)
        self.assertEqual(_askLocation.call_count, 1)
        self.assertEqual(_askPurchaseDate.call_count, 1)
        self.assertEqual(_askDebitDate.call_count, 0)
        self.assertEqual(_askInvoice.call_count, 1)
        self.assertEqual(_askNote.call_count, 1)
        self.assertEqual(_updateAccountAmount.call_count, 1)


    @patch.object(CreateRecordPage, "execute")
    @patch.object(CreateRecordPage, "choose",
        side_effect=[CreateRecordOption.INCOME, CreateRecordOption.EXPENSE, CreateRecordOption.BACK],
    )
    @patch.object(CreateRecordPage, "show")
    def test_start(self, _show, _choose, _execute):
        CreateRecordPage.start()
        self.assertEqual(_show.call_count, 3)
        self.assertEqual(_choose.call_count, 3)
        self.assertEqual(_execute.call_count, 2)

    