from unittest import TestCase
import mysqlConfig as cfg
import sqlalchemy as sql
from mock import patch
import const
from account import AccountCategory
from fixedIE import FixedIEType
from sqlalchemy_utils import database_exists, create_database, drop_database
from datetime import datetime
from freezegun import freeze_time

class MockDB(TestCase):

    config = cfg.test

    @classmethod
    @freeze_time("2023-05-18")
    def setUpClass(cls):
        if database_exists(cls.config['url']):
            drop_database(cls.config['url'])
            print("%sOriginal database %s dropped.%s" %
                  (const.ANSI_BLACK, cls.config['database'], const.ANSI_RESET))
        create_database(cls.config['url'])
        print("%sDatabase %s created.%s" %
              (const.ANSI_BLACK, cls.config['database'], const.ANSI_RESET))

        engine = sql.create_engine(cls.config['url'])
        conn = engine.connect()
        metadata = sql.MetaData()

        budget = sql.Table('Budget', metadata,
                         sql.Column(
                             'id', sql.Integer(), nullable=False, primary_key=True),
                         sql.Column(
                             'amount', sql.Float(), nullable=False)
                         )

        account = sql.Table('Account', metadata,
                         sql.Column(
                             'id', sql.Integer(), nullable=False, primary_key=True),
                         sql.Column(
                             'name', sql.String(50), nullable=False),
                         sql.Column(
                             'balance', sql.Float(), nullable=False),
                         sql.Column(
                             'category', sql.Enum(AccountCategory), default=AccountCategory.CASH, nullable=False)
                         )
        income = sql.Table('Income', metadata,
                        sql.Column('id', sql.Integer(), nullable=False, primary_key=True),
                        sql.Column('name', sql.String(50), nullable=False))

        category = sql.Table('Category', metadata,
                            sql.Column(
                                'id', sql.Integer(), nullable=False, primary_key=True),
                            sql.Column(
                                'name', sql.String(50), nullable=False)
                            )

        location = sql.Table('Location', metadata,
                             sql.Column(
                                 'id', sql.Integer(), nullable=False, primary_key=True),
                             sql.Column(
                                 'name', sql.String(50), nullable=False)
                             )

        fixedIE = sql.Table('FixedIE', metadata,
                        sql.Column(
                            'id', sql.Integer(), nullable=False, primary_key=True),
                        sql.Column(
                            'name', sql.String(50), nullable=False),
                        sql.Column(
                            'IE', sql.Enum(FixedIEType), nullable=False),
                        sql.Column(
                            'category', sql.String(30), nullable=False),
                        sql.Column(
                            'account', sql.String(30), nullable=False),
                        sql.Column(
                            'amount', sql.Float(), nullable=False),
                        sql.Column(
                            'location', sql.String(30), nullable=False),
                        sql.Column(
                            'day', sql.Integer(), nullable=False),
                        sql.Column(
                            'note', sql.String(30), nullable=True),
                        sql.Column(
                            'flag', sql.Boolean(), default=False, nullable=False)
        )

        record = sql.Table('Record', metadata,
                        sql.Column(
                            'id', sql.Integer(), nullable=False, primary_key=True),
                        sql.Column(
                            'IE', sql.Enum(FixedIEType), nullable=False),
                        sql.Column(
                            'category', sql.String(30), nullable=False),
                        sql.Column(
                            'account', sql.String(30), nullable=False),
                        sql.Column(
                            'amount', sql.Float(), nullable=False),
                        sql.Column(
                            'location', sql.String(30), nullable=False),
                        sql.Column(
                            'purchaseDate', sql.Date(), default=datetime.today(), nullable=False),
                        sql.Column(
                            'debitDate', sql.Date(), default=datetime.today(), nullable=False),
                        sql.Column(
                            'invoice', sql.String(30), nullable=True),
                        sql.Column(
                            'note', sql.String(30), nullable=True)
                        )

        metadata.create_all(engine)

        conn.execute(budget.insert().values(id=1, amount=10000.00))

        default_accounts = [
            {'name': "錢包", 'balance': 10000, 'category': AccountCategory.CASH.name},
            {'name': "中華郵政", 'balance': 25000, 'category': AccountCategory.DEBIT_CARD.name},
            {'name': "Line Pay", 'balance': 3000, 'category': AccountCategory.ELECTRONIC.name},
            {'name': "Line Pay", 'balance': 100, 'category': AccountCategory.ELECTRONIC.name},
        ]
        conn.execute(account.insert().values(default_accounts))

        default_incomes = [
            {'name': "獎金"},
            {'name': "退款"},
            {'name': "回饋"},
            {'name': "其他"}
        ]
        conn.execute(income.insert().values(default_incomes))

        default_fixedIE = [
            {'IE': FixedIEType.INCOME.name, 'name': "獎學金", 'category': "其它", 'account': "其它", 'amount': 10000, 'location': "其它", 'day': 15, 'note': '', 'flag': True},
            {'IE': FixedIEType.EXPENSE.name, 'name': "房租", 'category': "其它", 'account': "其它", 'amount': 6000, 'location': "其它", 'day': 20, 'note': 'sos', 'flag': False}
        ]
        conn.execute(fixedIE.insert().values(default_fixedIE))


        default_categories = [
            {'name': "食物"},
            {'name': "飲料"},
            {'name': "衣服"},
            {'name': "住宿"},
            {'name': "交通"},
            {'name': "其它"}
        ]
        conn.execute(category.insert().values(default_categories))

        default_locations = [
            {'name': "便利商店"},
            {'name': "蝦皮"},
            {'name': "誠品"},
            {'name': "夜市"},
            {'name': "其它"}
        ]
        conn.execute(location.insert().values(default_locations))

        default_records = [
            {'IE': "EXPENSE",'category': "食物", 'account': "現金", 'amount': 50, 'location': "便利商店", 'purchaseDate': '2023-05-01', 'debitDate': '2023-05-01', 'invoice': "12345678", 'note': "milk"},
            {'IE': "EXPENSE",'category': "住宿", 'account': "Line Pay", 'amount': 2500, 'location': "其它", 'purchaseDate': datetime.today().date(), 'debitDate': datetime.today().date(), 'invoice': "", 'note': "taipei"},
            {'IE': "INCOME",'category': "其它", 'account': "中華郵政", 'amount': 10000, 'location': "其它", 'purchaseDate': '2023-05-22', 'debitDate': '2023-05-23', 'invoice': "19970901", 'note': ""},
            {'IE': "EXPENSE",'category': "飲料", 'account': "Line Pay", 'amount': 100, 'location': "飲料店", 'purchaseDate': '2023-05-19', 'debitDate': '2023-05-19', 'invoice': "", 'note': "麻古-芝芝芒果"},
            {'IE': "EXPENSE",'category': "飲料", 'account': "現金", 'amount': 101, 'location': "comebuy", 'purchaseDate': '2023-01-01', 'debitDate': '2023-01-01', 'invoice': "", 'note': ""},
            {'IE': "EXPENSE",'category': "食物", 'account': "現金", 'amount': 87, 'location': "全家", 'purchaseDate': '2023-02-18', 'debitDate': '2023-02-18','invoice': "", 'note': ""},
            {'IE': "EXPENSE",'category': "衣服", 'account': "LinePay", 'amount': 321, 'location': "百貨公司", 'purchaseDate': '2023-03-05', 'debitDate': '2023-03-05','invoice': "", 'note': "洋裝"},
            {'IE': "EXPENSE",'category': "食物", 'account': "信用卡", 'amount': 70, 'location': "百貨公司", 'purchaseDate': '2023-03-28', 'debitDate': '2023-03-30','invoice': "", 'note': "coco"}
        ]
        conn.execute(record.insert().values(default_records))

        conn.commit()
        conn.close()

        cls.mock_db_config = patch.dict(cfg.dev, cfg.test)

    @classmethod
    def tearDownClass(cls):
        engine = sql.create_engine(cls.config['url'])
        metadata = sql.MetaData()
        metadata.drop_all(engine)
        drop_database(cls.config['url'])
        print("%sDatabase %s dropped.%s" %(const.ANSI_BLACK, cls.config['database'], const.ANSI_RESET))

