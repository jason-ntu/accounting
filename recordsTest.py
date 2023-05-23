import io
from unittest import TestCase
from unittest.mock import patch
from records import RecordPage, RecordOption
from mock_db import MockDB
from accessor import ExecutionStatus as es
import const
from createRecord import CreateRecordPage
from readRecord import ReadRecordPage
from updateRecord import UpdateRecordPage
from deleteRecord import DeleteRecordPage
from category import CategoryPage
from payment import PaymentPage
from location import LocationPage

class TestRecordPage(MockDB):

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['0', '6', 'T', '1', '2', '3', '4', '5'])
    def test_choose(self, _input,  _stdout):
        self.assertEqual(RecordPage.choose(), RecordOption.CREATE)
        self.assertEqual(_input.call_count, 4)
        self.assertEqual(RecordPage.choose(), RecordOption.READ)
        self.assertEqual(_input.call_count, 5)
        self.assertEqual(RecordPage.choose(), RecordOption.UPDATE)
        self.assertEqual(_input.call_count, 6)
        self.assertEqual(RecordPage.choose(), RecordOption.DELETE)
        self.assertEqual(_input.call_count, 7)
        self.assertEqual(RecordPage.choose(), RecordOption.BACK)
        self.assertEqual(_input.call_count, 8)
        self.assertEqual(_stdout.getvalue(), "請輸入 1 到 5 之間的數字:\n"*3)
    
    @patch.object(RecordPage, 'execute')
    @patch.object(RecordPage, 'choose', side_effect=[RecordOption.CREATE, RecordOption.READ, RecordOption.UPDATE, RecordOption.DELETE, RecordOption.BACK])
    @patch.object(RecordPage, 'show')
    def test_start(self, _show, _choose, _execute):
        RecordPage.start()
        self.assertEqual(_show.call_count, 5)
        self.assertEqual(_choose.call_count, 5)
        self.assertEqual(_execute.call_count, 4)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_show(self, _stdout):
        RecordPage.show()
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(len(output_lines), 5)
        self.assertEqual(output_lines[0], "%d: 新增消費紀錄" % RecordOption.CREATE)
        self.assertEqual(output_lines[1], "%d: 檢視消費紀錄" % RecordOption.READ)
        self.assertEqual(output_lines[2], "%d: 修改消費紀錄" % RecordOption.UPDATE)
        self.assertEqual(output_lines[3], "%d: 刪除消費紀錄" % RecordOption.DELETE)
        self.assertEqual(output_lines[4], "%d: 回到上一頁" % RecordOption.BACK)
    
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(DeleteRecordPage, 'start', return_value=False)
    @patch.object(UpdateRecordPage, 'start')
    @patch.object(ReadRecordPage, 'start', return_value=True)
    @patch.object(CreateRecordPage, 'start', return_value=True)
    def test_execute(self, _create, _read, _update, _delete, _stdout):
        with self.mock_db_config:
            RecordPage.execute(RecordOption.CREATE)
            self.assertEqual(_create.call_count, 1)
            RecordPage.execute(RecordOption.READ)
            self.assertEqual(_read.call_count, 1)
            RecordPage.execute(RecordOption.UPDATE)
            self.assertEqual(_update.call_count, 1)
            RecordPage.execute(RecordOption.DELETE)
            self.assertEqual(_delete.call_count, 1)
    
    @patch.object(RecordPage, 'hintRetryCategory')
    @patch.object(CategoryPage, 'getList', return_value=[["食物", "飲料", "衣服", "住宿", "交通", "其他"]])
    @patch.object(RecordPage, 'hintGetCategory')
    @patch.object(RecordPage, 'showCategory')
    @patch('builtins.input', side_effect=['0', 'T', '7', '1'])
    def test_askCategory(self, _input, _showCategory, _hintGetCategory, _getList, _hintRetryCategory):
        RecordPage.askCategory()
        self.assertEqual(_getList.call_count, 1)
        self.assertEqual(_showCategory.call_count, 1)
        self.assertEqual(_hintGetCategory.call_count, 1)
        self.assertEqual(_hintRetryCategory.call_count, 3)
        self.assertEqual(_input.call_count, 4)

    @patch.object(RecordPage, 'hintRetryPayment')
    @patch.object(PaymentPage, 'getList', return_value=[["錢包", "儲蓄卡", "信用卡", "Line Pay", "Metamask"]])
    @patch.object(RecordPage, 'hintGetPayment')
    @patch.object(RecordPage, 'showPayment')
    @patch('builtins.input', side_effect=['0', 'T', '6', '1'])
    def test_askPayment(self, _input, _showPayment, _hintGetPayment, _getList, _hintRetryPayment):
        RecordPage.askPayment()
        self.assertEqual(_getList.call_count, 1)
        self.assertEqual(_showPayment.call_count, 1)
        self.assertEqual(_hintGetPayment.call_count, 1)
        self.assertEqual(_hintRetryPayment.call_count, 3)
        self.assertEqual(_input.call_count, 4)
    
    @patch.object(RecordPage, 'hintNumberErorMsg')
    @patch.object(RecordPage, 'hintGetAmount')
    @patch('builtins.input', side_effect=['-1', 'T', '50'])
    def test_askAmount(self, _input, _hintGetAmount, _hintNumberErorMsg):
        RecordPage.askAmount()
        self.assertEqual(_hintGetAmount.call_count, 1)
        self.assertEqual(_hintNumberErorMsg.call_count, 2)
        self.assertEqual(_input.call_count, 3)

    @patch.object(RecordPage, 'hintRetryLocation')
    @patch.object(LocationPage, 'getList', return_value=[["餐廳", "飲料店", "超商", "超市", "夜市", "文具店", "線上商店", "百貨公司", "學校", "其它"]])
    @patch.object(RecordPage, 'hintGetLocation')
    @patch.object(RecordPage, 'showLocation')
    @patch('builtins.input', side_effect=['0', 'T', '11', '1'])
    def test_askLocation(self, _input, _showLocation, _hintGetLocation, _getList, _hintRetryLocation):
        RecordPage.askLocation()
        self.assertEqual(_getList.call_count, 1)
        self.assertEqual(_showLocation.call_count, 1)
        self.assertEqual(_hintGetLocation.call_count, 1)
        self.assertEqual(_hintRetryLocation.call_count, 3)
        self.assertEqual(_input.call_count, 4)

    @patch.object(RecordPage, 'hintGetPurchaseDate')
    @patch('builtins.input', side_effect=["", "T", "2023/05/20", "2023-05-25"])
    def test_askPurchaseDate(self, _input, _hintGetPurchaseDate):
        RecordPage.askPurchaseDate()
        self.assertEqual(_hintGetPurchaseDate.call_count, 1)
        self.assertEqual(_input.call_count, 1)
        RecordPage.askPurchaseDate()
        self.assertEqual(_hintGetPurchaseDate.call_count, 4)
        self.assertEqual(_input.call_count, 4)

    @patch.object(RecordPage, 'hintGetDebitDate')
    @patch('builtins.input', side_effect=["", "T", "2023/05/20", "2023-05-25"])
    def test_askDebitDate(self, _input, _hintGetDebitDate):
        RecordPage.askDebitDate()
        self.assertEqual(_hintGetDebitDate.call_count, 1)
        self.assertEqual(_input.call_count, 1)
        RecordPage.askDebitDate()
        self.assertEqual(_hintGetDebitDate.call_count, 4)
        self.assertEqual(_input.call_count, 4)

    @patch.object(RecordPage, 'hintGetInvoice')
    @patch('builtins.input', side_effect=["", "T", "JK970901", "12345678"])
    def test_askInvoice(self, _input, _hintGetInvoice):
        RecordPage.askInvoice()
        self.assertEqual(_hintGetInvoice.call_count, 1)
        self.assertEqual(_input.call_count, 1)
        RecordPage.askInvoice()
        self.assertEqual(_hintGetInvoice.call_count, 4)
        self.assertEqual(_input.call_count, 4)
    
    @patch.object(RecordPage, 'hintGetNote')
    @patch('builtins.input', side_effect=["", "好吃"])
    def test_askNote(self, _input, _hintGetNote):
        RecordPage.askNote()
        self.assertEqual(_hintGetNote.call_count, 1)
        self.assertEqual(_input.call_count, 1)
        RecordPage.askNote()
        self.assertEqual(_hintGetNote.call_count, 2)
        self.assertEqual(_input.call_count, 2)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_hints(self, _stdout):
        hints = [(RecordPage.hintGetCategory, "請輸入紀錄類型:\n"),
                (RecordPage.hintRetryCategory, "請輸入 1 到 1 之間的數字:\n"),
                 (RecordPage.hintRetryPayment, "請輸入 1 到 1 之間的數字:\n"),
                 (RecordPage.hintRetryAmount, "請輸入大於0的數字:\n"),
                 (RecordPage.hintRetryLocation, "請輸入 1 到 1 之間的數字:\n"),
                 (RecordPage.hintNumberErorMsg, "請輸入數字:\n"),
                 (RecordPage.hintGetPayment, "請輸入收支方式:\n"),
                 (RecordPage.hintGetAmount, "請輸入金額:\n"),
                 (RecordPage.hintGetLocation, "請輸入消費地點:\n"),
                 (RecordPage.hintGetPurchaseDate, "請輸入消費日期(yyyy-mm-dd):\n"),
                 (RecordPage.hintGetDebitDate, "請輸入扣款日期(yyyy-mm-dd):\n"),
                 (RecordPage.hintGetNote, "請輸入備註:\n"),
                 (RecordPage.hintGetInvoice, "請輸入發票末八碼數字:\n")]
        for hint in hints:
            hint[0]()
            self.assertMultiLineEqual(_stdout.getvalue(), hint[1])
            _stdout.truncate(0)
            _stdout.seek(0)