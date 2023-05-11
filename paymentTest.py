import io
from unittest.mock import patch
from payment import PaymentPage, PaymentOption
from mock_db import MockDB
from accessor import ExecutionStatus as es
import const

class TestPaymentPage(MockDB):

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_show(self, _stdout):
        PaymentPage.show()
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "%d: 新增支付方式" % PaymentOption.CREATE)
        self.assertEqual(output_lines[1], "%d: 查看支付方式" % PaymentOption.READ)
        self.assertEqual(output_lines[2], "%d: 修改支付方式" % PaymentOption.UPDATE)
        self.assertEqual(output_lines[3], "%d: 刪除支付方式" % PaymentOption.DELETE)
        self.assertEqual(output_lines[4], "%d: 回到上一頁" % PaymentOption.BACK)
    
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_hints(self, _stdout):
        hints = [(PaymentPage.hint_create_name, "請輸入新支付方式的...\n名稱:\n"),
                 (PaymentPage.hint_create_balance, "餘額:\n"),
                 (PaymentPage.hint_create_category, "類型(1 現金, 2 借記卡, 3 信用卡, 4 電子支付, 5 其他):\n"),
                 (PaymentPage.hint_update_name, "請選擇要修改的支付方式(輸入名稱):\n"),
                 (PaymentPage.hint_update_option, "請選擇要修改的項目(1 名稱, 2 餘額, 3 類型):\n"),
                 (PaymentPage.hint_update_new_name, "請輸入新的名稱:\n"),
                 (PaymentPage.hint_update_new_balance, "請輸入新的餘額:\n"),
                 (PaymentPage.hint_update_new_category, "請輸入新的類型(1 現金, 2 借記卡, 3 信用卡, 4 電子支付, 5 其他):\n"),
                 (PaymentPage.hint_delete, "請選擇要刪除的支付方式(輸入名稱):\n")]
        for hint in hints:
            hint[0]()
            self.assertMultiLineEqual(_stdout.getvalue(), hint[1])
            _stdout.truncate(0)
            _stdout.seek(0)
    
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['0', '6', 'T', '1', '2', '3', '4', '5'])
    def test_choose(self, _input,  _stdout):
        self.assertEqual(PaymentPage.choose(), PaymentOption.CREATE)
        self.assertEqual(_input.call_count, 4)
        self.assertEqual(_stdout.getvalue(), "請輸入 1 到 5 之間的數字:\n"*3)
        self.assertEqual(PaymentPage.choose(), PaymentOption.READ)
        self.assertEqual(_input.call_count, 5)
        self.assertEqual(PaymentPage.choose(), PaymentOption.UPDATE)
        self.assertEqual(_input.call_count, 6)
        self.assertEqual(PaymentPage.choose(), PaymentOption.DELETE)
        self.assertEqual(_input.call_count, 7)
        self.assertEqual(PaymentPage.choose(), PaymentOption.BACK)
        self.assertEqual(_input.call_count, 8)
    
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(PaymentPage, 'delete', return_value=True)
    @patch.object(PaymentPage, 'update', return_value=False)
    @patch.object(PaymentPage, 'read')
    @patch.object(PaymentPage, 'create', return_value=True)
    def test_execute(self, _create, _read, _update, _delete, _stdout):
        with self.mock_db_config:
            PaymentPage.execute(PaymentOption.CREATE)
            self.assertEqual(_create.call_count, 1)
            PaymentPage.execute(PaymentOption.READ)
            self.assertEqual(_read.call_count, 1)
            PaymentPage.execute(PaymentOption.UPDATE)
            self.assertEqual(_update.call_count, 1)
            PaymentPage.execute(PaymentOption.DELETE)
            self.assertEqual(_delete.call_count, 1)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "%s操作成功%s" %
                         (const.ANSI_GREEN, const.ANSI_RESET))
        self.assertEqual(output_lines[1], "%s操作失敗%s" %
                         (const.ANSI_RED, const.ANSI_RESET))
        self.assertEqual(output_lines[2], "%s操作成功%s" %
                         (const.ANSI_GREEN, const.ANSI_RESET))
    
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=["冷錢包", "一萬", 10000, 6, 5])
    @patch.object(PaymentPage, 'hint_create_category')
    @patch.object(PaymentPage, 'hint_create_balance')
    @patch.object(PaymentPage, 'hint_create_name')
    def test_create(self, _hint_create_name, _hint_create_balance, _hint_create_category, _input, _stdout):
        with self.mock_db_config:
            PaymentPage.setUp_connection_and_table()
            PaymentPage.create()
            PaymentPage.tearDown_connection(es.NONE)
        self.assertEqual(_hint_create_name.call_count, 1)
        self.assertEqual(_hint_create_balance.call_count, 1)
        self.assertEqual(_hint_create_category.call_count, 1)
        self.assertEqual(_input.call_count, 5)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "請輸入數字:")
        self.assertEqual(output_lines[1], "請輸入 1 到 5 之間的數字:")

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read(self, _stdout):
        with self.mock_db_config:
            PaymentPage.setUp_connection_and_table()
            PaymentPage.read()
            PaymentPage.tearDown_connection(es.NONE)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "\"錢包\" 剩餘 10000.0 元，支付類型為 CASH")
        self.assertEqual(output_lines[1], "\"中華郵政\" 剩餘 25000.0 元，支付類型為 DEBIT_CARD")
        self.assertEqual(output_lines[2], "\"Line Pay\" 剩餘 3000.0 元，支付類型為 ELECTRONIC")
        self.assertEqual(output_lines[3], "\"Line Pay\" 剩餘 100.0 元，支付類型為 ELECTRONIC")

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=["錢包", 0, 1, "皮夾", "Line Pay", 2, 'F', 5000, "unknown", 3, 6, 5])
    @patch.object(PaymentPage, 'hint_update_new_category')
    @patch.object(PaymentPage, 'hint_update_new_balance')
    @patch.object(PaymentPage, 'hint_update_new_name')
    @patch.object(PaymentPage, 'hint_update_option')
    @patch.object(PaymentPage, 'hint_update_name')
    def test_update(self, _hint_update_name, _hint_update_option, _hint_update_new_name, _hint_update_new_balance, _hint_update_new_category, _input, _stdout):
        with self.mock_db_config:
            PaymentPage.setUp_connection_and_table()
            self.assertEqual(PaymentPage.update(), True)
            PaymentPage.read()

            self.assertEqual(PaymentPage.update(), False)
            PaymentPage.read()

            self.assertEqual(PaymentPage.update(), False)
            PaymentPage.read()

            PaymentPage.tearDown_connection(es.NONE)

        self.assertEqual(_hint_update_name.call_count, 3)
        self.assertEqual(_hint_update_option.call_count, 3)
        self.assertEqual(_hint_update_new_name.call_count, 1)
        self.assertEqual(_hint_update_new_balance.call_count, 1)
        self.assertEqual(_hint_update_new_category.call_count, 1)
        self.assertEqual(_input.call_count, 12)

        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "請輸入 1 到 3 之間的數字:")
        self.assertEqual(output_lines[1], "\"皮夾\" 剩餘 10000.0 元，支付類型為 CASH")
        self.assertEqual(output_lines[2], "\"中華郵政\" 剩餘 25000.0 元，支付類型為 DEBIT_CARD")
        self.assertEqual(output_lines[3], "\"Line Pay\" 剩餘 3000.0 元，支付類型為 ELECTRONIC")
        self.assertEqual(output_lines[4], "\"Line Pay\" 剩餘 100.0 元，支付類型為 ELECTRONIC")
        self.assertEqual(output_lines[5], "請輸入數字:")
        self.assertEqual(output_lines[6], "%sLine Pay 對應到多個支付方式%s" % (
            const.ANSI_YELLOW, const.ANSI_RESET))
        self.assertEqual(output_lines[7], "\"皮夾\" 剩餘 10000.0 元，支付類型為 CASH")
        self.assertEqual(output_lines[8], "\"中華郵政\" 剩餘 25000.0 元，支付類型為 DEBIT_CARD")
        # FIXME 不同支付方式有重複名稱的處理有些奇怪，
        self.assertEqual(output_lines[9], "\"Line Pay\" 剩餘 5000.0 元，支付類型為 ELECTRONIC")
        self.assertEqual(output_lines[10], "\"Line Pay\" 剩餘 5000.0 元，支付類型為 ELECTRONIC")
        self.assertEqual(output_lines[11], "請輸入 1 到 5 之間的數字:")
        self.assertEqual(output_lines[12], "%sunknown 對應不到任何支付方式%s" % (
            const.ANSI_YELLOW, const.ANSI_RESET))
        self.assertEqual(output_lines[13], "\"皮夾\" 剩餘 10000.0 元，支付類型為 CASH")
        self.assertEqual(output_lines[14], "\"中華郵政\" 剩餘 25000.0 元，支付類型為 DEBIT_CARD")
        self.assertEqual(output_lines[15], "\"Line Pay\" 剩餘 5000.0 元，支付類型為 ELECTRONIC")
        self.assertEqual(output_lines[16], "\"Line Pay\" 剩餘 5000.0 元，支付類型為 ELECTRONIC")
    
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=["Line Pay", "unknown", "中華郵政"])
    @patch.object(PaymentPage, 'hint_delete')
    def test_delete(self, _hint_delete, _input, _stdout):
        with self.mock_db_config:
            PaymentPage.setUp_connection_and_table()
            self.assertEqual(PaymentPage.delete(), True)
            PaymentPage.read()
            self.assertEqual(PaymentPage.delete(), False)
            PaymentPage.read()
            self.assertEqual(PaymentPage.delete(), True)
            PaymentPage.read()
            PaymentPage.tearDown_connection(es.NONE)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "\"錢包\" 剩餘 10000.0 元，支付類型為 CASH")
        self.assertEqual(output_lines[1], "\"中華郵政\" 剩餘 25000.0 元，支付類型為 DEBIT_CARD")
        self.assertEqual(output_lines[2], "%sunknown 對應不到任何支付方式%s" % (
            const.ANSI_YELLOW, const.ANSI_RESET))
        self.assertEqual(output_lines[3], "\"錢包\" 剩餘 10000.0 元，支付類型為 CASH")
        self.assertEqual(output_lines[4], "\"中華郵政\" 剩餘 25000.0 元，支付類型為 DEBIT_CARD")
        self.assertEqual(output_lines[5], "\"錢包\" 剩餘 10000.0 元，支付類型為 CASH")
            
    @patch.object(PaymentPage, 'execute')
    @patch.object(PaymentPage, 'choose', side_effect=[PaymentOption.CREATE, PaymentOption.READ, PaymentOption.UPDATE, PaymentOption.DELETE, PaymentOption.BACK])
    @patch.object(PaymentPage, 'show')
    def test_start(self, _show, _choose, _execute):
        PaymentPage.start()
        self.assertEqual(_show.call_count, 5)
        self.assertEqual(_choose.call_count, 5)
        self.assertEqual(_execute.call_count, 4)
