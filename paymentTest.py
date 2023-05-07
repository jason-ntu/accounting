import io
from unittest.mock import patch
from payment import PaymentPage, PaymentOption
from mock_db import MockDB


class TestPaymentPage(MockDB):
        
    def setUp(self) -> None:
        self.paymentPage = PaymentPage()

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_show(self, _stdout):
        self.paymentPage.show()
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "%d: 新增支付方式" % PaymentOption.CREATE)
        self.assertEqual(output_lines[1], "%d: 查看支付方式" % PaymentOption.READ)
        self.assertEqual(output_lines[2], "%d: 修改支付方式" % PaymentOption.UPDATE)
        self.assertEqual(output_lines[3], "%d: 刪除支付方式" % PaymentOption.DELETE)
        self.assertEqual(output_lines[4], "%d: 回到上一頁" % PaymentOption.BACK)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['0', '6', 'T', '1', '2', '3', '4', '5'])
    def test_choose(self, _input,  _stdout):
        self.assertEqual(self.paymentPage.choose(), 1)
        self.assertEqual(_input.call_count, 4)
        self.assertEqual(_stdout.getvalue(), "請輸入 1 到 5 之間的數字:\n"*3)
        self.assertEqual(self.paymentPage.choose(), 2)
        self.assertEqual(_input.call_count, 5)
        self.assertEqual(self.paymentPage.choose(), 3)
        self.assertEqual(_input.call_count, 6)
        self.assertEqual(self.paymentPage.choose(), 4)
        self.assertEqual(_input.call_count, 7)
        self.assertEqual(self.paymentPage.choose(), 5)
        self.assertEqual(_input.call_count, 8)
    
    @patch.object(PaymentPage, 'delete')
    @patch.object(PaymentPage, 'update')
    @patch.object(PaymentPage, 'read')
    @patch.object(PaymentPage, 'create')
    def test_execute(self, _create, _read, _update, _delete):
        self.paymentPage.execute(PaymentOption.CREATE)
        self.assertEqual(_create.call_count, 1)
        self.paymentPage.execute(PaymentOption.READ)
        self.assertEqual(_read.call_count, 1)
        self.paymentPage.execute(PaymentOption.UPDATE)
        self.assertEqual(_update.call_count, 1)
        self.paymentPage.execute(PaymentOption.DELETE)
        self.assertEqual(_delete.call_count, 1)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_hint_create_name(self, _stdout):
        self.paymentPage.hint_create_name()
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "請輸入新支付方式的...")
        self.assertEqual(output_lines[1], "名稱:")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_hint_create_balance(self, _stdout):
        self.paymentPage.hint_create_balance()
        self.assertEqual(_stdout.getvalue(), "餘額:\n")
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_hint_create_category(self, _stdout):
        self.paymentPage.hint_create_category()
        self.assertEqual(_stdout.getvalue(), "類型(1 現金, 2 借記卡, 3 信用卡, 4 電子支付, 5 其他):\n")
        
    # def test_read(self):
    #     with self.mock_db_config:
    #         self.assertEqual(self.paymentPage.read(), 10000)

    # @patch('builtins.input', side_effect=['XYZ', 12345])
    # @patch.object(balancePage, 'hint')
    # def test_update(self, _hint, _input):
    #     with self.mock_db_config:
    #         self.assertEqual(self.paymentPage.update(), True)
    #         self.assertEqual(self.paymentPage.read(), 12345)
    #     self.assertEqual(_hint.call_count, 1)
    #     self.assertEqual(_input.call_count, 2)
    
    # @patch('sys.stdout', new_callable=io.StringIO)
    # def test_hint(self, _stdout):
    #     self.paymentPage.hint()
    #     self.assertEqual(_stdout.getvalue(), "請輸入新的總預算:\n")

    # @patch.object(balancePage, 'execute')
    # @patch.object(balancePage, 'choose', side_effect=[PaymentOption.READ, PaymentOption.UPDATE, PaymentOption.BACK])
    # @patch.object(balancePage, 'show')
    # def test_start(self, _show, _choose, _execute):
    #     self.paymentPage.start()
    #     self.assertEqual(_show.call_count, 3)
    #     self.assertEqual(_choose.call_count, 3)
    #     self.assertEqual(_execute.call_count, 2)
