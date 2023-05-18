import io
from unittest.mock import patch
from location import LocationPage, LocationOption
from mock_db import MockDB
from accessor import ExecutionStatus as es
import const


class TestLocationPage(MockDB):

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_show(self, _stdout):
        LocationPage.show()
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "%d: 新增地點" % LocationOption.CREATE)
        self.assertEqual(output_lines[1], "%d: 查看地點" % LocationOption.READ)
        self.assertEqual(output_lines[2], "%d: 修改地點" % LocationOption.UPDATE)
        self.assertEqual(output_lines[3], "%d: 刪除地點" % LocationOption.DELETE)
        self.assertEqual(output_lines[4], "%d: 回到上一頁" % LocationOption.BACK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_hints(self, _stdout):
        hints = [(LocationPage.hint_create_name, "請輸入新地點的名稱:\n"),
                 (LocationPage.hint_update_name, "請輸入要修改的地點名稱:\n"),
                 (LocationPage.hint_update_new_name, "請輸入新的名稱:\n"),
                 (LocationPage.hint_delete, "請輸入要刪除的地點名稱:\n")]
        for hint in hints:
            hint[0]()
            self.assertMultiLineEqual(_stdout.getvalue(), hint[1])
            _stdout.truncate(0)
            _stdout.seek(0)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['0', '6', 'T', '1', '2', '3', '4', '5'])
    def test_choose(self, _input,  _stdout):
        self.assertEqual(LocationPage.choose(), LocationOption.CREATE)
        self.assertEqual(_input.call_count, 4)
        self.assertEqual(_stdout.getvalue(), "請輸入 1 到 5 之間的數字:\n"*3)
        self.assertEqual(LocationPage.choose(), LocationOption.READ)
        self.assertEqual(_input.call_count, 5)
        self.assertEqual(LocationPage.choose(), LocationOption.UPDATE)
        self.assertEqual(_input.call_count, 6)
        self.assertEqual(LocationPage.choose(), LocationOption.DELETE)
        self.assertEqual(_input.call_count, 7)
        self.assertEqual(LocationPage.choose(), LocationOption.BACK)
        self.assertEqual(_input.call_count, 8)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(LocationPage, 'delete', return_value=True)
    @patch.object(LocationPage, 'update', return_value=False)
    @patch.object(LocationPage, 'read')
    @patch.object(LocationPage, 'create', return_value=True)
    def test_execute(self, _create, _read, _update, _delete, _stdout):
        with self.mock_db_config:
            LocationPage.execute(LocationOption.CREATE)
            self.assertEqual(_create.call_count, 1)
            LocationPage.execute(LocationOption.READ)
            self.assertEqual(_read.call_count, 1)
            LocationPage.execute(LocationOption.UPDATE)
            self.assertEqual(_update.call_count, 1)
            LocationPage.execute(LocationOption.DELETE)
            self.assertEqual(_delete.call_count, 1)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "%s操作成功%s" %
                         (const.ANSI_GREEN, const.ANSI_RESET))
        self.assertEqual(output_lines[1], "%s操作失敗%s" %
                         (const.ANSI_RED, const.ANSI_RESET))
        self.assertEqual(output_lines[2], "%s操作成功%s" %
                         (const.ANSI_GREEN, const.ANSI_RESET))

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=["", "便利商店", "學校", 123])
    @patch.object(LocationPage, 'hint_create_name')
    def test_create(self, _hint_create_name, _input, _stdout):
        results = [False, False, True, True]
        outputs = ["%s名稱不得為空%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET),
                   "%s名稱不得與其它地點的名稱重複%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET), "", ""]
        for i in range(3):
            with self.mock_db_config:
                LocationPage.setUp_connection_and_table()
                result = LocationPage.create()
                # LocationPage.read()
                LocationPage.tearDown_connection(es.NONE)
            self.assertEqual(result, results[i])
            self.assertEqual(_hint_create_name.call_count, i+1)
            self.assertEqual(_input.call_count, i+1)
            self.assertEqual(_stdout.getvalue(), outputs[i])
            _stdout.truncate(0)
            _stdout.seek(0)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read(self, _stdout):
        with self.mock_db_config:
            LocationPage.setUp_connection_and_table()
            LocationPage.read()
            LocationPage.tearDown_connection(es.NONE)
        output_lines = _stdout.getvalue().strip().split('\n')
        locations = ["便利商店", "蝦皮", "誠品", "夜市", "其它"]
        for i in range(len(output_lines)):
            self.assertEqual(output_lines[i], locations[i])

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=[
        # pairs of input for 5 cases
        "百貨公司", "商場",
        "蝦皮", "",
        "便利商店", "夜市",
        "誠品", "誠品",
        "蝦皮", "淘寶"])
    @patch.object(LocationPage, 'hint_update_new_name')
    @patch.object(LocationPage, 'hint_update_name')
    def test_update(self, _hint_update_name, _hint_update_new_name, _input, _stdout):
        results = [False, False, False, True, True]
        outputs = [
            "%s目前沒有這個地點%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET),
            "%s新名稱不得為空%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET),
            "%s新名稱不得與其它地點的名稱重複%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET),
            "",
            ""
            ]
        
        for i in range(5):
            with self.mock_db_config:
                LocationPage.setUp_connection_and_table()
                result = LocationPage.update()
                # LocationPage.read()
                LocationPage.tearDown_connection(es.NONE)
            self.assertEqual(result, results[i])
            self.assertEqual(_hint_update_name.call_count, i+1)
            self.assertEqual(_hint_update_new_name.call_count, i+1)
            self.assertEqual(_input.call_count, 2*i+2)
            self.assertEqual(_stdout.getvalue(), outputs[i])
            _stdout.truncate(0)
            _stdout.seek(0)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=["", "unknown", "蝦皮"])
    @patch.object(LocationPage, 'hint_delete')
    def test_delete(self, _hint_delete, _input, _stdout):
        results = [False, False, True]
        outputs = ["%s名稱不得為空%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET),
                   "%s目前沒有這個地點%s\n" % (const.ANSI_YELLOW, const.ANSI_RESET),
                   ""]
        for i in range(3):
            with self.mock_db_config:
                LocationPage.setUp_connection_and_table()
                result = LocationPage.delete()
                # LocationPage.read()
                LocationPage.tearDown_connection(es.NONE)
            self.assertEqual(result, results[i])
            self.assertEqual(_hint_delete.call_count, i+1)
            self.assertEqual(_input.call_count, i + 1)
            self.assertEqual(_stdout.getvalue(), outputs[i])
            _stdout.truncate(0)
            _stdout.seek(0)

    @patch.object(LocationPage, 'execute')
    @patch.object(LocationPage, 'choose', side_effect=[LocationOption.CREATE, LocationOption.READ, LocationOption.UPDATE, LocationOption.DELETE, LocationOption.BACK])
    @patch.object(LocationPage, 'show')
    def test_start(self, _show, _choose, _execute):
        LocationPage.start()
        self.assertEqual(_show.call_count, 5)
        self.assertEqual(_choose.call_count, 5)
        self.assertEqual(_execute.call_count, 4)
