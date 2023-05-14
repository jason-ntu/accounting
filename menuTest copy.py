from unittest import TestCase
from unittest.mock import patch
from menu import MenuPage, MenuOption, MenuText
import io
from records import RecordPage
from report import ReportPage
#from export import ExportPage
from setting import SettingPage


class TestMenuPage(TestCase):

    def setUp(self):
        self.menuPage = MenuPage()

    @patch.object(MenuPage, 'go')
    @patch.object(MenuPage, 'choose', side_effect = [MenuOption.RECORD, MenuOption.REPORT, MenuOption.EXPORT, MenuOption.SETTING, MenuOption.CLOSE])
    @patch.object(MenuPage, 'show')
    def test_start(self, m_show, m_choose, m_go):
        self.menuPage.start()
        # print('m_show.call_count >> ' + str(m_show.call_count))
        # print('m_choose.call_count >> ' + str(m_choose.call_count))
        # print('m_go.call_count >> ' + str(m_go.call_count))
        self.assertEqual(m_show.call_count, 5)
        self.assertEqual(m_choose.call_count, 5)
        self.assertEqual(m_go.call_count, 4)

    @patch("sys.stdout", new_callable = io.StringIO)
    def test_show(self, m_stdout):
        self.menuPage.show()
        outputLines = m_stdout.getvalue().strip().split('\n')
        self.assertEqual(outputLines[1], str(MenuText.RECORD))
        self.assertEqual(outputLines[2], str(MenuText.REPORT))
        self.assertEqual(outputLines[3], str(MenuText.EXPORT))
        self.assertEqual(outputLines[4], str(MenuText.SETTING))
        self.assertEqual(outputLines[5], str(MenuText.CLOSE))

    @patch("builtins.input", side_effect=["7", "1", "2", "3", "4", "T", "5"])
    @patch("sys.stdout", new_callable = io.StringIO)
    def test_choose(self, m_stdout, m_input):
        #self.assertEqual(m_stdout.getvalue(), MenuText.HINT)
        self.assertEqual(self.menuPage.choose(), MenuOption.RECORD)
        self.assertEqual(self.menuPage.choose(), MenuOption.REPORT)
        self.assertEqual(self.menuPage.choose(), MenuOption.EXPORT)
        self.assertEqual(self.menuPage.choose(), MenuOption.SETTING)
        self.assertEqual(self.menuPage.choose(), MenuOption.CLOSE)
        self.assertEqual(m_input.call_count, 7)
        #print(m_stdout.getvalue())        
        #print(m_input.call_count)
        #print('m_input.call_count >> ' + str(m_input.call_count))

    @patch.object(SettingPage, 'start')
    #@patch.object(ExportPage, 'start')
    @patch.object(ReportPage, 'start')
    @patch.object(RecordPage, 'start')
    def test_go(self, m_recordStart, m_reportStart, m_settingStart):
        self.menuPage.go(MenuOption.RECORD)
        self.assertEqual(m_recordStart.call_count, 1)
        self.menuPage.go(MenuOption.REPORT)
        self.assertEqual(m_reportStart.call_count, 1)
        # self.menuPage.go(MenuOption.EXPORT)
        # self.assertEqual(m_exportStart.call_count, 1)
        self.menuPage.go(MenuOption.SETTING)
        self.assertEqual(m_settingStart.call_count, 1)      
