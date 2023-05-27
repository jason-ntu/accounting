import io
import unittest
from unittest.mock import patch
from IEAttribute import IEAttribute, Operation, IEOption
from mock_db import MockDB
from accessor import ExecutionStatus as es
import const



class TestLocationPage(MockDB):
    
    def setUp(self):
        IEAttribute.table_name = "IEAttribute"
    
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_hints(self, _stdout):
        hints = [(IEAttribute.hintGetOperation, "1: 新增收支屬性\n2: 查看收支屬性\n3: 修改收支屬性\n4: 刪除收支屬性\n5: 回到上一頁\n"),
                 (IEAttribute.hint_create_name, "請輸入新屬性的名稱:\n"),
                 (IEAttribute.hint_update_name, "請輸入要修改的屬性名稱:\n"),
                 (IEAttribute.hint_update_new_name, "請輸入新的名稱:\n"),
                 (IEAttribute.hint_delete, "請輸入要刪除的屬性名稱:\n"),
                 (IEAttribute.hintGetIE, "請問要操作收入屬性還是支出屬性:\n1: 收入\n2: 支出\n3: 回到上一頁\n")]
        for hint in hints:
            hint[0]()
            self.assertMultiLineEqual(_stdout.getvalue(), hint[1])
            _stdout.truncate(0)
            _stdout.seek(0)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['0', '6', 'T', '1', '2', '3', '4', '5'])
    def test_chooseOperation(self, _input, _stdout):
        self.assertEqual(IEAttribute.chooseOperation(), Operation.CREATE)
        self.assertEqual(_input.call_count, 4)
        self.assertEqual(_stdout.getvalue(), "請輸入 1 到 5 之間的數字:\n"*3)
        self.assertEqual(IEAttribute.chooseOperation(), Operation.READ)
        self.assertEqual(_input.call_count, 5)
        self.assertEqual(IEAttribute.chooseOperation(), Operation.UPDATE)
        self.assertEqual(_input.call_count, 6)
        self.assertEqual(IEAttribute.chooseOperation(), Operation.DELETE)
        self.assertEqual(_input.call_count, 7)
        self.assertEqual(IEAttribute.chooseOperation(), Operation.BACK)
        self.assertEqual(_input.call_count, 8)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(IEAttribute, 'delete', return_value=True)
    @patch.object(IEAttribute, 'update', return_value=False)
    @patch.object(IEAttribute, 'read')
    @patch.object(IEAttribute, 'create', return_value=True)
    def test_execute(self, _create, _read, _update, _delete, _stdout):
        with self.mock_db_config:
            IEAttribute.execute(Operation.CREATE)
            IEAttribute.execute(Operation.READ)
            IEAttribute.execute(Operation.UPDATE)
            IEAttribute.execute(Operation.DELETE)
        self.assertEqual(_create.call_count, 1)
        self.assertEqual(_read.call_count, 1)
        self.assertEqual(_update.call_count, 1)
        self.assertEqual(_delete.call_count, 1)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "%s操作成功%s" %
                         (const.ANSI_GREEN, const.ANSI_RESET))
        self.assertEqual(output_lines[1], "%s操作失敗%s" %
                         (const.ANSI_RED, const.ANSI_RESET))
        self.assertEqual(output_lines[2], "%s操作成功%s" %
                         (const.ANSI_GREEN, const.ANSI_RESET))

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=[
        "",
        "選項A",
        "選項B",
        123])
    @patch.object(IEAttribute, 'hint_create_name')
    def test_create(self, _hint_create_name, _input, _stdout):
        IEAttribute.IE = IEOption.INCOME
        results = [False, False, True, True]
        outputs = [f"{const.ANSI_YELLOW}新屬性的名稱不得為空{const.ANSI_RESET}\n",
                   f"{const.ANSI_YELLOW}新屬性的名稱不得與既有屬性的名稱重複{const.ANSI_RESET}\n",
                   "",
                   ""]
        for i in range(4):
            with self.mock_db_config:
                IEAttribute.setUp_connection_and_table()
                result = IEAttribute.create()
                # LocationPage.read()
                IEAttribute.tearDown_connection(es.NONE)
            self.assertEqual(result, results[i])
            self.assertEqual(_hint_create_name.call_count, i+1)
            self.assertEqual(_input.call_count, i+1)
            self.assertEqual(_stdout.getvalue(), outputs[i])
            _stdout.truncate(0)
            _stdout.seek(0)
    
    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_read(self, _stdout):
    #     with self.mock_db_config:
    #         LocationPage.setUp_connection_and_table()
    #         LocationPage.read()
    #         LocationPage.tearDown_connection(es.NONE)
    #     output_lines = _stdout.getvalue().strip().split('\n')
    #     locations = ["公司 INCOME",
    #     "學校 INCOME",
    #     "家裡 INCOME",
    #     "政府 INCOME",
    #     "銀行 INCOME",
    #     "其它 INCOME",
    #     "餐廳 EXPENSE",
    #     "飲料店 EXPENSE",
    #     "超商 EXPENSE",
    #     "超市 EXPENSE",
    #     "夜市 EXPENSE",
    #     "文具店 EXPENSE",
    #     "線上商店 EXPENSE",
    #     "百貨公司 EXPENSE",
    #     "學校 EXPENSE",
    #     "其它 EXPENSE"]
    #     for i, line in enumerate(output_lines):
    #         self.assertEqual(line, locations[i])

    # @unittest.skip('TODO')
    # @patch("sys.stdout", new_callable=io.StringIO)
    # @patch('builtins.input', side_effect=[
    #     # pairs of input for 5 cases
    #     "百貨公司", "商場",
    #     "蝦皮", "",
    #     "便利商店", "夜市",
    #     "誠品", "誠品",
    #     "蝦皮", "淘寶"])
    # @patch.object(LocationPage, 'hint_update_new_name')
    # @patch.object(LocationPage, 'hint_update_name')
    # def test_update(self, _hint_update_name, _hint_update_new_name, _input, _stdout):
    #     results = [False, False, False, True, True]
    #     outputs = [
    #         "%s目前沒有這個地點%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET),
    #         "%s新名稱不得為空%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET),
    #         "%s新名稱不得與其它地點的名稱重複%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET),
    #         "",
    #         ""
    #         ]
        
    #     for i in range(5):
    #         with self.mock_db_config:
    #             LocationPage.setUp_connection_and_table()
    #             result = LocationPage.update()
    #             # LocationPage.read()
    #             LocationPage.tearDown_connection(es.NONE)
    #         self.assertEqual(result, results[i])
    #         self.assertEqual(_hint_update_name.call_count, i+1)
    #         self.assertEqual(_hint_update_new_name.call_count, i+1)
    #         self.assertEqual(_input.call_count, 2*i+2)
    #         self.assertEqual(_stdout.getvalue(), outputs[i])
    #         _stdout.truncate(0)
    #         _stdout.seek(0)

    # @unittest.skip('TODO')
    # @patch("sys.stdout", new_callable=io.StringIO)
    # @patch('builtins.input', side_effect=["", "unknown", "蝦皮"])
    # @patch.object(LocationPage, 'hint_delete')
    # def test_delete(self, _hint_delete, _input, _stdout):
    #     results = [False, False, True]
    #     outputs = ["%s名稱不得為空%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET),
    #                "%s目前沒有這個地點%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET),
    #                ""]
    #     for i in range(3):
    #         with self.mock_db_config:
    #             LocationPage.setUp_connection_and_table()
    #             result = LocationPage.delete()
    #             # LocationPage.read()
    #             LocationPage.tearDown_connection(es.NONE)
    #         self.assertEqual(result, results[i])
    #         self.assertEqual(_hint_delete.call_count, i+1)
    #         self.assertEqual(_input.call_count, i + 1)
    #         self.assertEqual(_stdout.getvalue(), outputs[i])
    #         _stdout.truncate(0)
    #         _stdout.seek(0)

    # @patch.object(LocationPage, 'execute')
    # @patch.object(LocationPage, 'choose', side_effect=[LocationOption.CREATE, LocationOption.READ, LocationOption.UPDATE, LocationOption.DELETE, LocationOption.BACK])
    # @patch.object(LocationPage, 'show')
    # def test_start(self, _show, _choose, _execute):
    #     LocationPage.start()
    #     self.assertEqual(_show.call_count, 5)
    #     self.assertEqual(_choose.call_count, 5)
    #     self.assertEqual(_execute.call_count, 4)

    # def test_getList(self):
    #     with self.mock_db_config:
    #         incomeLocationList = LocationPage.getList('INCOME')
    #         expenseLocationList = LocationPage.getList('EXPENSE')
    #     self.assertEqual(incomeLocationList, ['公司', '學校', '家裡', '政府', '銀行', '其它'])
    #     self.assertEqual(expenseLocationList, ['餐廳', '飲料店', '超商', '超市', '夜市', '文具店', '線上商店', '百貨公司', '學校', '其它'])
