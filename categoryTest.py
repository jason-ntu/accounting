import io
from unittest.mock import patch
from category import CategoryPage, CategoryOption
from mock_db import MockDB
from accessor import ExecutionStatus as es
import const

class TestCategoryPage(MockDB):

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_show(self, _stdout):
        CategoryPage.show()
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "%d: 新增類別" % CategoryOption.CREATE)
        self.assertEqual(output_lines[1], "%d: 查看類別" % CategoryOption.READ)
        self.assertEqual(output_lines[2], "%d: 修改類別" % CategoryOption.UPDATE)
        self.assertEqual(output_lines[3], "%d: 刪除類別" % CategoryOption.DELETE)
        self.assertEqual(output_lines[4], "%d: 回到上一頁" % CategoryOption.BACK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_hints(self, _stdout):
        hints = [(CategoryPage.hint_create_name, "請輸入新類別的名稱:\n"),
                 (CategoryPage.hint_update_name, "請選擇要修改的類別(輸入名稱):\n"),
                 (CategoryPage.hint_update_new_name, "請輸入新的名稱:\n"),
                 (CategoryPage.hint_delete, "請選擇要刪除的類別(輸入名稱):\n")]
        for hint in hints:
            hint[0]()
            self.assertMultiLineEqual(_stdout.getvalue(), hint[1])
            _stdout.truncate(0)
            _stdout.seek(0)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['0', '6', 'T', '1', '2', '3', '4', '5'])
    def test_choose(self, _input,  _stdout):
        self.assertEqual(CategoryPage.choose(), CategoryOption.CREATE)
        self.assertEqual(_input.call_count, 4)
        self.assertEqual(_stdout.getvalue(), "請輸入 1 到 5 之間的數字:\n"*3)
        self.assertEqual(CategoryPage.choose(), CategoryOption.READ)
        self.assertEqual(_input.call_count, 5)
        self.assertEqual(CategoryPage.choose(), CategoryOption.UPDATE)
        self.assertEqual(_input.call_count, 6)
        self.assertEqual(CategoryPage.choose(), CategoryOption.DELETE)
        self.assertEqual(_input.call_count, 7)
        self.assertEqual(CategoryPage.choose(), CategoryOption.BACK)
        self.assertEqual(_input.call_count, 8)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(CategoryPage, 'delete', return_value=True)
    @patch.object(CategoryPage, 'update', return_value=False)
    @patch.object(CategoryPage, 'read')
    @patch.object(CategoryPage, 'create', return_value=True)
    def test_execute(self, _create, _read, _update, _delete, _stdout):
        with self.mock_db_config:
            CategoryPage.execute(CategoryOption.CREATE)
            self.assertEqual(_create.call_count, 1)
            CategoryPage.execute(CategoryOption.READ)
            self.assertEqual(_read.call_count, 1)
            CategoryPage.execute(CategoryOption.UPDATE)
            self.assertEqual(_update.call_count, 1)
            CategoryPage.execute(CategoryOption.DELETE)
            self.assertEqual(_delete.call_count, 1)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "%s操作成功%s" %
                         (const.ANSI_GREEN, const.ANSI_RESET))
        self.assertEqual(output_lines[1], "%s操作失敗%s" %
                         (const.ANSI_RED, const.ANSI_RESET))
        self.assertEqual(output_lines[2], "%s操作成功%s" %
                         (const.ANSI_GREEN, const.ANSI_RESET))

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=["", "食物", "文具", 123])
    @patch.object(CategoryPage, 'hint_create_name')
    def test_create(self, _hint_create_name, _input, _stdout):
        results = [False, False, True, True]
        outputs = ["%s名稱不得為空%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET),
                   "%s名稱不得與其他類別的名稱重複%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET), "", ""]
        for i in range(3):
            with self.mock_db_config:
                CategoryPage.setUp_connection_and_table()
                result = CategoryPage.create()
                # CategoryPage.read()
                CategoryPage.tearDown_connection(es.NONE)
            self.assertEqual(result, results[i])
            self.assertEqual(_hint_create_name.call_count, i+1)
            self.assertEqual(_input.call_count, i+1)
            self.assertEqual(_stdout.getvalue(), outputs[i])
            _stdout.truncate(0)
            _stdout.seek(0)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read(self, _stdout):
        with self.mock_db_config:
            CategoryPage.setUp_connection_and_table()
            CategoryPage.read()
            CategoryPage.tearDown_connection(es.NONE)
        output_lines = _stdout.getvalue().strip().split('\n')
        categories = ["食物", "飲料", "衣服", "住宿", "交通"]
        for i in range(5):
            self.assertEqual(output_lines[i], categories[i])

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=["文具", "交通", "", "食物", "飲料", "衣服", "衣服", "飲料", "下午茶"])
    @patch.object(CategoryPage, 'hint_update_new_name')
    @patch.object(CategoryPage, 'hint_update_name')
    def test_update(self, _hint_update_name, _hint_update_new_name, _input, _stdout):
        results = [False, False, False, True, True]
        outputs = ["%s目前沒有這個類別%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET),
                   "%s新名稱不得為空%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET), 
                   "%s新名稱不得與其他類別的名稱重複%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET), "", ""]
        for i in range(5):
            with self.mock_db_config:
                CategoryPage.setUp_connection_and_table()
                result = CategoryPage.update()
                # CategoryPage.read()
                CategoryPage.tearDown_connection(es.NONE)
            self.assertEqual(result, results[i])
            self.assertEqual(_hint_update_name.call_count, i+1)
            self.assertEqual(_hint_update_new_name.call_count, i)
            self.assertEqual(_input.call_count, 2*i + 1)
            self.assertEqual(_stdout.getvalue(), outputs[i])
            _stdout.truncate(0)
            _stdout.seek(0)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=["", "unknown", "食物"])
    @patch.object(CategoryPage, 'hint_delete')
    def test_delete(self, _hint_delete, _input, _stdout):
        results = [False, False, True]
        outputs = ["%s名稱不得為空%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET),
                   "%s目前沒有這個類別%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET),
                   ""]
        for i in range(3):
            with self.mock_db_config:
                CategoryPage.setUp_connection_and_table()
                result = CategoryPage.delete()
                # CategoryPage.read()
                CategoryPage.tearDown_connection(es.NONE)
            self.assertEqual(result, results[i])
            self.assertEqual(_hint_delete.call_count, i+1)
            self.assertEqual(_input.call_count, i + 1)
            self.assertEqual(_stdout.getvalue(), outputs[i])
            _stdout.truncate(0)
            _stdout.seek(0)

    @patch.object(CategoryPage, 'execute')
    @patch.object(CategoryPage, 'choose', side_effect=[CategoryOption.CREATE, CategoryOption.READ, CategoryOption.UPDATE, CategoryOption.DELETE, CategoryOption.BACK])
    @patch.object(CategoryPage, 'show')
    def test_start(self, _show, _choose, _execute):
        CategoryPage.start()
        self.assertEqual(_show.call_count, 5)
        self.assertEqual(_choose.call_count, 5)
        self.assertEqual(_execute.call_count, 4)
