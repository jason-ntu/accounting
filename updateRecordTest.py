import io
from unittest import TestCase
from unittest.mock import patch
from updateRecord import UpdateRecordPage, ItemOption
from mock_db import MockDB
from accessor import ExecutionStatus as es
import const
from records import RecordOption, RecordPage
from readRecord import ReadRecordPage, ReadRecordOption

class TestUpdateRecord(MockDB):

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_hints(self, _stdout):
        hints = [(UpdateRecordPage.hintChooseItem, "1 收入支出 2 類別 3 帳戶 4 金額 5 地點 6 消費時間 7 扣款時間 8 發票號碼 9 備註\n請輸入要更改的項目:\n"),
                 (UpdateRecordPage.hintGetCategory, "請輸入新的紀錄類型:\n"),
                 (UpdateRecordPage.hintGetAccount, "請輸入新的帳戶:\n"),
                 (UpdateRecordPage.hintGetAmount, "請輸入新的金額:\n"),
                 (UpdateRecordPage.hintGetLocation, "請輸入新的消費地點:\n"),
                 (UpdateRecordPage.hintGetPurchaseDate, "請輸入新的消費日期(yyyy-mm-dd):\n"),
                 (UpdateRecordPage.hintGetDebitDate, "請輸入新的扣款日期(yyyy-mm-dd):\n"),
                 (UpdateRecordPage.hintGetNote, "請輸入新的備註:\n"),
                 (UpdateRecordPage.hintGetInvoice, "請輸入新的發票號碼(發票末8碼數字):\n"),
                 (UpdateRecordPage.hintGetID, "請輸入想更改的紀錄ID:\n")]
        for hint in hints:
            hint[0]()
            self.assertMultiLineEqual(_stdout.getvalue(), hint[1])
            _stdout.truncate(0)
            _stdout.seek(0)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(UpdateRecordPage, 'hintChooseItem')
    @patch("builtins.input", side_effect=["1", "F", "10", "2.5", "9"])
    def test_chooseItem(self, _input, _hintChooseItem, _stdout):
        UpdateRecordPage.chooseItem()
        self.assertEqual(_input.call_count, 1)
        UpdateRecordPage.chooseItem()
        self.assertEqual(_input.call_count, 5)
        self.assertEqual(_hintChooseItem.call_count, 5)
        self.assertEqual(_stdout.getvalue(), "請輸入 1 到 9 之間的數字:\n"*3)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["2.5", "F", "1", "2"])
    def test_checkIDInteger(self, _input, _stdout):
        self.assertEqual(UpdateRecordPage.checkIDInteger(), 1)
        self.assertEqual(_input.call_count, 3)
        self.assertEqual(UpdateRecordPage.checkIDInteger(), 2)
        self.assertEqual(_input.call_count, 4)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(len(output_lines), 6)
        self.assertEqual(output_lines[0], "請輸入想更改的紀錄ID:")
        self.assertEqual(output_lines[1],"輸入的ID須為整數")
        self.assertEqual(output_lines[2], "請輸入想更改的紀錄ID:")
        self.assertEqual(output_lines[3],"輸入的ID須為整數")
        self.assertEqual(output_lines[4], "請輸入想更改的紀錄ID:")
        self.assertEqual(output_lines[5], "請輸入想更改的紀錄ID:")
    

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(UpdateRecordPage, 'askCategory', return_value=["食物"])
    def test_updateCategory(self, _askCategory, _stdout):
        with self.mock_db_config:
            UpdateRecordPage.setUp_connection_and_table()
            UpdateRecordPage.updateCategory(1)
            UpdateRecordPage.updateCategory(20)
            UpdateRecordPage.tearDown_connection(es.NONE)
        self.assertEqual(_askCategory.call_count, 1)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(len(output_lines), 3)
        self.assertEqual(output_lines[0], "%s操作成功%s" % (const.ANSI_GREEN, const.ANSI_RESET))
        self.assertEqual(output_lines[1], "此紀錄ID不存在")
        self.assertEqual(output_lines[2], "%s操作失敗%s" % (const.ANSI_RED, const.ANSI_RESET))
    
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(UpdateRecordPage, 'askAccount', return_value={'name': '儲蓄卡', 'category': 'DEBIT_CARD'})
    def test_updateAccount(self, _askAccount, _stdout):
        with self.mock_db_config:
            UpdateRecordPage.setUp_connection_and_table()
            UpdateRecordPage.updateAccount(1)
            UpdateRecordPage.updateAccount(20)
            UpdateRecordPage.tearDown_connection(es.NONE)
        self.assertEqual(_askAccount.call_count, 2)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(len(output_lines), 3)
        self.assertEqual(output_lines[0], "%s操作成功%s" % (const.ANSI_GREEN, const.ANSI_RESET))
        self.assertEqual(output_lines[1], "此紀錄ID不存在")
        self.assertEqual(output_lines[2], "%s操作失敗%s" % (const.ANSI_RED, const.ANSI_RESET))
    
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(UpdateRecordPage, 'askAmount', return_value=[100])
    def test_updateAmount(self, _askAmount, _stdout):
        with self.mock_db_config:
            UpdateRecordPage.setUp_connection_and_table()
            UpdateRecordPage.updateAmount(1)
            UpdateRecordPage.updateAmount(20)
            UpdateRecordPage.tearDown_connection(es.NONE)
        self.assertEqual(_askAmount.call_count, 2)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(len(output_lines), 3)
        self.assertEqual(output_lines[0], "%s操作成功%s" % (const.ANSI_GREEN, const.ANSI_RESET))
        self.assertEqual(output_lines[1], "此紀錄ID不存在")
        self.assertEqual(output_lines[2], "%s操作失敗%s" % (const.ANSI_RED, const.ANSI_RESET))
    
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(UpdateRecordPage, 'askLocation', return_value=["便利商店"])
    def test_updateLocation(self, _askLocation, _stdout):
        with self.mock_db_config:
            UpdateRecordPage.setUp_connection_and_table()
            UpdateRecordPage.updateLocation(1)
            UpdateRecordPage.updateLocation(20)
            UpdateRecordPage.tearDown_connection(es.NONE)
        self.assertEqual(_askLocation.call_count, 2)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(len(output_lines), 3)
        self.assertEqual(output_lines[0], "%s操作成功%s" % (const.ANSI_GREEN, const.ANSI_RESET))
        self.assertEqual(output_lines[1], "此紀錄ID不存在")
        self.assertEqual(output_lines[2], "%s操作失敗%s" % (const.ANSI_RED, const.ANSI_RESET))
    
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(UpdateRecordPage, 'askIE', return_value=1)
    def test_updateIE(self, _askIE, _stdout):
        with self.mock_db_config:
            UpdateRecordPage.setUp_connection_and_table()
            UpdateRecordPage.updateIE(1)
            UpdateRecordPage.updateIE(20)
            UpdateRecordPage.tearDown_connection(es.NONE)
        self.assertEqual(_askIE.call_count, 2)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(len(output_lines), 3)
        self.assertEqual(output_lines[0], "%s操作成功%s" % (const.ANSI_GREEN, const.ANSI_RESET))
        self.assertEqual(output_lines[1], "此紀錄ID不存在")
        self.assertEqual(output_lines[2], "%s操作失敗%s" % (const.ANSI_RED, const.ANSI_RESET))
    
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(UpdateRecordPage, 'askPurchaseDate', return_value="2023-05-20")
    def test_updatePurchaseDate(self, _askPurchaseDate, _stdout):
        with self.mock_db_config:
            UpdateRecordPage.setUp_connection_and_table()
            UpdateRecordPage.updatePurchaseDate(1)
            UpdateRecordPage.updatePurchaseDate(20)
            UpdateRecordPage.tearDown_connection(es.NONE)
        self.assertEqual(_askPurchaseDate.call_count, 2)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(len(output_lines), 3)
        self.assertEqual(output_lines[0], "%s操作成功%s" % (const.ANSI_GREEN, const.ANSI_RESET))
        self.assertEqual(output_lines[1], "此紀錄ID不存在")
        self.assertEqual(output_lines[2], "%s操作失敗%s" % (const.ANSI_RED, const.ANSI_RESET))
    
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(UpdateRecordPage, 'askDebitDate', return_value="2023-05-20")
    def test_updateDebitDate(self, _askDebitDate, _stdout):
        with self.mock_db_config:
            UpdateRecordPage.setUp_connection_and_table()
            UpdateRecordPage.updateDebitDate(1)
            UpdateRecordPage.updateDebitDate(20)
            UpdateRecordPage.tearDown_connection(es.NONE)
        self.assertEqual(_askDebitDate.call_count, 2)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(len(output_lines), 3)
        self.assertEqual(output_lines[0], "%s操作成功%s" % (const.ANSI_GREEN, const.ANSI_RESET))
        self.assertEqual(output_lines[1], "此紀錄ID不存在")
        self.assertEqual(output_lines[2], "%s操作失敗%s" % (const.ANSI_RED, const.ANSI_RESET))
    

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(UpdateRecordPage, 'askInvoice', return_value="")
    def test_updateInvoice(self, _askInvoice, _stdout):
        with self.mock_db_config:
            UpdateRecordPage.setUp_connection_and_table()
            UpdateRecordPage.updateInvoice(1)
            UpdateRecordPage.updateInvoice(20)
            UpdateRecordPage.tearDown_connection(es.NONE)
        self.assertEqual(_askInvoice.call_count, 2)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(len(output_lines), 3)
        self.assertEqual(output_lines[0], "%s操作成功%s" % (const.ANSI_GREEN, const.ANSI_RESET))
        self.assertEqual(output_lines[1], "此紀錄ID不存在")
        self.assertEqual(output_lines[2], "%s操作失敗%s" % (const.ANSI_RED, const.ANSI_RESET))
    
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(UpdateRecordPage, 'askNote', return_value="")
    def test_updateNote(self, _askNote, _stdout):
        with self.mock_db_config:
            UpdateRecordPage.setUp_connection_and_table()
            UpdateRecordPage.updateNote(1)
            UpdateRecordPage.updateNote(20)
            UpdateRecordPage.tearDown_connection(es.NONE)
        self.assertEqual(_askNote.call_count, 2)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(len(output_lines), 3)
        self.assertEqual(output_lines[0], "%s操作成功%s" % (const.ANSI_GREEN, const.ANSI_RESET))
        self.assertEqual(output_lines[1], "此紀錄ID不存在")
        self.assertEqual(output_lines[2], "%s操作失敗%s" % (const.ANSI_RED, const.ANSI_RESET))
    
    @patch.object(UpdateRecordPage, 'updateNote', return_value="")
    @patch.object(UpdateRecordPage, 'updateInvoice', return_value="")
    @patch.object(UpdateRecordPage, 'updateDebitDate', return_value="")
    @patch.object(UpdateRecordPage, 'updatePurchaseDate', return_value="")
    @patch.object(UpdateRecordPage, 'updateLocation', return_value="")
    @patch.object(UpdateRecordPage, 'updateAmount', return_value="")
    @patch.object(UpdateRecordPage, 'updateAccount', return_value="")
    @patch.object(UpdateRecordPage, 'updateCategory', return_value="")
    @patch.object(UpdateRecordPage, 'updateIE', return_value="")
    def test_updateDB(self, _IE, _Category, _Account, _Amount, _Location, __Purchase, _Debit, _Invoice, _Note):
        UpdateRecordPage.updateDB(1, ItemOption.IE)
        self.assertEqual(_IE.call_count, 1)
        UpdateRecordPage.updateDB(1, ItemOption.CATEGORY)
        self.assertEqual(_Category.call_count, 1)
        UpdateRecordPage.updateDB(1, ItemOption.ACCOUNT)
        self.assertEqual(_Account.call_count, 1)
        UpdateRecordPage.updateDB(1, ItemOption.AMOUNT)
        self.assertEqual(_Amount.call_count, 1)
        UpdateRecordPage.updateDB(1, ItemOption.LOCATION)
        self.assertEqual(_Location.call_count, 1)
        UpdateRecordPage.updateDB(1, ItemOption.CONSUMPTIONTIME)
        self.assertEqual(__Purchase.call_count, 1)
        UpdateRecordPage.updateDB(1, ItemOption.DEDUCTIONTIME)
        self.assertEqual(_Debit.call_count, 1)
        UpdateRecordPage.updateDB(1, ItemOption.INVOICE)
        self.assertEqual(_Invoice.call_count, 1)
        UpdateRecordPage.updateDB(1, ItemOption.NOTE)
        self.assertEqual(_Note.call_count, 1)

    @patch.object(UpdateRecordPage, "updateDB")
    @patch.object(UpdateRecordPage, "chooseItem", return_value=1)
    @patch.object(UpdateRecordPage, "checkIDInteger")
    def test_updateByID(self, _checkIDInteger, _chooseItem, _updateDB):
        with self.mock_db_config:
            UpdateRecordPage.setUp_connection_and_table()
            UpdateRecordPage.updateByID()
            UpdateRecordPage.tearDown_connection(es.NONE)
        self.assertEqual(_checkIDInteger.call_count, 1)
        self.assertEqual(_chooseItem.call_count, 1)
        self.assertEqual(_updateDB.call_count, 1)
    
    @patch.object(UpdateRecordPage, "updateByID")
    @patch.object(ReadRecordPage, "execute")
    @patch.object(ReadRecordPage, "choose",
        side_effect=[ReadRecordOption.TODAY, ReadRecordOption.WEEK, ReadRecordOption.MONTH, ReadRecordOption.OTHER, ReadRecordOption.BACK],
    )
    @patch.object(ReadRecordPage, "show")
    def test_start(self, _show, _choose, _execute, _updateByID):
        UpdateRecordPage.start()
    #     self.assertEqual(_show.call_count, 5)
        # self.assertEqual(_choose.call_count, 5)
        # self.assertEqual(_execute.call_count, 4)
        # self.assertEqual(_updateByID.call_count, 4)
