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
from account import AccountPage
from location import LocationPage
import sqlalchemy as sql

class TestAccountPage(MockDB):

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

    @patch.object(RecordPage, 'hintGetIE')
    @patch('builtins.input', side_effect=['T', '3', '0', '1'])
    def test_askIE(self, _input, _hintGetIE):
        RecordPage.askIE()
        self.assertEqual(_input.call_count, 4)

    @patch.object(RecordPage, 'hintRetryAccount')
    @patch.object(AccountPage, 'getList', return_value=[["錢包", "儲蓄卡", "信用卡", "Line Pay", "Metamask"]])
    @patch.object(RecordPage, 'hintGetAccount')
    @patch.object(RecordPage, 'showAccount')
    @patch('builtins.input', side_effect=['0', 'T', '6', '1'])
    def test_askAccount(self, _input, _showAccount, _hintGetAccount, _getList, _hintRetryAccount):
        RecordPage.askAccount()
        self.assertEqual(_getList.call_count, 1)
        self.assertEqual(_showAccount.call_count, 1)
        self.assertEqual(_hintGetAccount.call_count, 1)
        self.assertEqual(_hintRetryAccount.call_count, 3)
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

    @patch.object(AccountPage, "show")
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=[
        # read and then back
        2, 5,
        # call updateAccountAmount...
        # read and then back
        2, 5
        ])
    def test_updateAccountAmount(self, _input, _stdout, _show):
        with self.mock_db_config:
            AccountPage.start()
            output_before = _stdout.getvalue().strip().split('\n')[0]
            _stdout.truncate(0)
            _stdout.seek(0)
            RecordPage.setUp_connection_and_table([RecordPage.table_name, AccountPage.table_name])
            RecordPage.updateAccountAmount('EXPENSE', '錢包', 100)
            output_result = _stdout.getvalue().strip().split('\n')[0]
            _stdout.truncate(0)
            _stdout.seek(0)
            AccountPage.start()
            output_after = _stdout.getvalue().strip().split('\n')[0]
            _stdout.truncate(0)
            _stdout.seek(0)
        
        expected_outputs = [
            # "1: 新增支付方式",
            # "2: 查看支付方式",
            # "3: 修改支付方式",
            # "4: 刪除支付方式",
            # "5: 回到上一頁",
            "\"錢包\" 剩餘 10000.0 元，支付類型為 CASH",
            # "\"中華郵政\" 剩餘 25000.0 元，支付類型為 DEBIT_CARD",
            # "\"Line Pay\" 剩餘 3000.0 元，支付類型為 ELECTRONIC",
            # "\"Line Pay\" 剩餘 100.0 元，支付類型為 ELECTRONIC"
            # "1: 新增支付方式",
            # "2: 查看支付方式",
            # "3: 修改支付方式",
            # "4: 刪除支付方式",
            # "5: 回到上一頁"
            f"{const.ANSI_GREEN}操作成功{const.ANSI_RESET}",
            # "1: 新增支付方式",
            # "2: 查看支付方式",
            # "3: 修改支付方式",
            # "4: 刪除支付方式",
            # "5: 回到上一頁",
            "\"錢包\" 剩餘 9900.0 元，支付類型為 CASH",
            # "\"中華郵政\" 剩餘 25000.0 元，支付類型為 DEBIT_CARD",
            # "\"Line Pay\" 剩餘 3000.0 元，支付類型為 ELECTRONIC",
            # "\"Line Pay\" 剩餘 100.0 元，支付類型為 ELECTRONIC"
            # "1: 新增支付方式",
            # "2: 查看支付方式",
            # "3: 修改支付方式",
            # "4: 刪除支付方式",
            # "5: 回到上一頁"
        ]

        self.assertEqual(output_before, expected_outputs[0])
        self.assertEqual(output_result, expected_outputs[1])
        self.assertEqual(output_after, expected_outputs[2])
            

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_hints(self, _stdout):
        hints = [(RecordPage.hintGetCategory, "請輸入紀錄類型:\n"),
                (RecordPage.hintRetryCategory, "請輸入 1 到 1 之間的數字:\n"),
                 (RecordPage.hintRetryAccount, "請輸入 1 到 1 之間的數字:\n"),
                 (RecordPage.hintRetryAmount, "請輸入大於0的數字:\n"),
                 (RecordPage.hintRetryLocation, "請輸入 1 到 1 之間的數字:\n"),
                 (RecordPage.hintNumberErorMsg, "請輸入數字:\n"),
                 (RecordPage.hintGetAccount, "請輸入帳戶:\n"),
                 (RecordPage.hintGetAmount, "請輸入金額:\n"),
                 (RecordPage.hintGetLocation, "請輸入消費地點:\n"),
                 (RecordPage.hintGetPurchaseDate, "請輸入消費日期(yyyy-mm-dd):\n"),
                 (RecordPage.hintGetDebitDate, "請輸入扣款日期(yyyy-mm-dd):\n"),
                 (RecordPage.hintGetNote, "請輸入備註:\n"),
                 (RecordPage.hintGetIE, "1 收入 2 支出\n請選擇新的收入/支出:\n"),
                 (RecordPage.hintGetInvoice, "請輸入發票末八碼數字:\n")]
        for hint in hints:
            hint[0]()
            self.assertMultiLineEqual(_stdout.getvalue(), hint[1])
            _stdout.truncate(0)
            _stdout.seek(0)

    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_updateAccountAmount(self, _stdout):
    #     with self.mock_db_config:
    #         RecordPage.setUp_connection_and_table(["Record"])
    #         RecordPage.updateAccountAmount("EXPENSE", "現金", 100)
    #         query = sql.select(RecordPage.tables[0].c['amount']).where(RecordPage.tables[0].c.account == "現金")
    #         result = RecordPage.conn.execute(query).fetchone()
    #         RecordPage.tearDown_connection(es.NONE)
        