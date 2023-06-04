import io
from unittest.mock import patch
from IEAttribute import IEAttribute, Operation, IEOption
from mock_db import MockDB
from accessor import ExecutionStatus as es
import const



class TestLocationPage(MockDB):
    
    def setUp(self):
        IEAttribute.table_name = "IEAttribute"
        IEAttribute.IE = IEOption.INCOME
    
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
                IEAttribute.tearDown_connection(es.NONE)
            self.assertEqual(result, results[i])
            self.assertEqual(_hint_create_name.call_count, i+1)
            self.assertEqual(_input.call_count, i+1)
            self.assertEqual(_stdout.getvalue(), outputs[i])
            _stdout.truncate(0)
            _stdout.seek(0)
    
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read(self, _stdout):
        with self.mock_db_config:
            IEAttribute.setUp_connection_and_table()
            IEAttribute.read()
            IEAttribute.tearDown_connection(es.NONE)
        self.assertEqual(_stdout.getvalue(), "選項A\n選項C\n")

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=[
        # For logic testing in this function,
        # CC, PC, and CACC are all covered.
        #     C1: len(results) > 0
        #     C2: name != new_name
        #     P: C1 and C2
        #                     C1   C2   P
        "選項B", "選項D",     # F    T   F
        "選項A", "",         # F    T   F
        "選項A", "選項C",     # T    T   T
        "選項A", "選項A",     # T    F   F
        "選項A", "選項D"])    # F    T   F 
    @patch.object(IEAttribute, 'hint_update_new_name')
    @patch.object(IEAttribute, 'hint_update_name')
    def test_update(self, _hint_update_name, _hint_update_new_name, _input, _stdout):
        results = [False, False, False, True, True]
        outputs = [
            "%s目前沒有這個屬性%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET),
            "%s新名稱不得為空%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET),
            "%s新名稱不得與既有屬性的名稱重複%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET),
            "",
            ""
            ]
        for i in range(5):
            with self.mock_db_config:
                IEAttribute.setUp_connection_and_table()
                result = IEAttribute.update()
                IEAttribute.tearDown_connection(es.NONE)
            self.assertEqual(result, results[i])
            self.assertEqual(_hint_update_name.call_count, i+1)
            self.assertEqual(_hint_update_new_name.call_count, i+1)
            self.assertEqual(_input.call_count, 2*i+2)
            self.assertEqual(_stdout.getvalue(), outputs[i])
            _stdout.truncate(0)
            _stdout.seek(0)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=[
        "",
        "unknown",
        "選項A"]
        )
    @patch.object(IEAttribute, 'hint_delete')
    def test_delete(self, _hint_delete, _input, _stdout):
        results = [False, False, True]
        outputs = ["%s名稱不得為空%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET),
                   "%s目前沒有這個屬性%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET),
                   ""]
        for i in range(3):
            with self.mock_db_config:
                IEAttribute.setUp_connection_and_table()
                result = IEAttribute.delete()
                IEAttribute.tearDown_connection(es.NONE)
            self.assertEqual(result, results[i])
            self.assertEqual(_hint_delete.call_count, i+1)
            self.assertEqual(_input.call_count, i + 1)
            self.assertEqual(_stdout.getvalue(), outputs[i])
            _stdout.truncate(0)
            _stdout.seek(0)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['X', 0, 1, 2, 4, 3])
    def test_chooseIE(self, _input, _stdout):
        errMsg = f"請輸入 1 到 {len(IEOption)} 之間的數字:\n"
        result = IEAttribute.chooseIE()
        self.assertEqual(_stdout.getvalue(), errMsg*2)
        _stdout.truncate(0)
        _stdout.seek(0)
        self.assertEqual(result, IEOption.INCOME)

        result = IEAttribute.chooseIE()
        self.assertEqual(result , IEOption.EXPENSE)

        result = IEAttribute.chooseIE()
        self.assertEqual(_stdout.getvalue(), errMsg)
        _stdout.truncate(0)
        _stdout.seek(0)
        self.assertEqual(result, IEOption.BACK)


    @patch.object(IEAttribute, 'execute')
    @patch.object(IEAttribute, 'chooseOperation', side_effect=[Operation.READ, Operation.CREATE, Operation.BACK, Operation.READ, Operation.UPDATE, Operation.DELETE, Operation.BACK])
    @patch.object(IEAttribute, 'hintGetOperation')
    @patch.object(IEAttribute, 'chooseIE', side_effect=[IEOption.INCOME, IEOption.EXPENSE, Operation.BACK])
    @patch.object(IEAttribute, 'hintGetIE')
    def test_start(self, _hintGetIE, _chooseIE, _hintGetOperation, _chooseOperation, _execute):
        IEAttribute.start()
        self.assertEqual(_hintGetIE.call_count, 3)
        self.assertEqual(_chooseIE.call_count, 3)
        self.assertEqual(_hintGetOperation.call_count, 7)
        self.assertEqual(_chooseOperation.call_count, 7)
        self.assertEqual(_execute.call_count, 5)

    def test_getList(self):
        with self.mock_db_config:
            incomeLocationList = IEAttribute.getList('INCOME')
            expenseLocationList = IEAttribute.getList('EXPENSE')
        self.assertEqual(incomeLocationList, ['選項A', '選項C'])
        self.assertEqual(expenseLocationList, ['選項B'])