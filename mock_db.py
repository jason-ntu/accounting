from unittest import TestCase
import mysqlConfig as cfg
import sqlalchemy as sql
from mock import patch
import const
from account import AccountCategory
from IEDirection import IEDirection
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

        end_time = sql.Table('EndTime', metadata,
                          sql.Column(
                            'id', sql.Integer(), nullable=False,primary_key=True),
                          sql.Column(
                            'time', sql.DateTime(), nullable=False)
                        )

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
        
        category = sql.Table('Category', metadata,
                    sql.Column(
                        'id', sql.Integer(), nullable=False, primary_key=True),
                    sql.Column(
                        'name', sql.String(50), nullable=False),
                    sql.Column(
                        'IE', sql.Enum(IEDirection), nullable=False)
                    )

        location = sql.Table('Location', metadata,
                    sql.Column(
                        'id', sql.Integer(), nullable=False, primary_key=True),
                    sql.Column(
                        'name', sql.String(50), nullable=False),
                    sql.Column(
                        'IE', sql.Enum(IEDirection), nullable=False)
                    )

        fixedIE = sql.Table('FixedIE', metadata,
                        sql.Column(
                            'id', sql.Integer(), nullable=False, primary_key=True),
                        sql.Column(
                            'name', sql.String(50), nullable=False),
                        sql.Column(
                            'IE', sql.Enum(IEDirection), nullable=False),
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
                            'registerTime', sql.DateTime(), nullable=False),
                        sql.Column(
                            'flag', sql.Boolean(), default=False, nullable=False)
        )

        record = sql.Table('Record', metadata,
                        sql.Column(
                            'id', sql.Integer(), nullable=False, primary_key=True),
                        sql.Column(
                            'IE', sql.Enum(IEDirection), nullable=False),
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
        
        IEAttribute = sql.Table('IEAttribute', metadata,
                        sql.Column(
                            'id', sql.Integer(), nullable=False, primary_key=True),
                        sql.Column(
                                 'name', sql.String(50), nullable=False),
                            sql.Column(
                                'IE', sql.Enum(IEDirection), nullable=False)
                        )

        metadata.create_all(engine)

        conn.execute(budget.insert().values(id=1, amount=10000.00))

        default_end_time = [
            {'time': datetime(2023, 5, 4, 0, 13, 45)}
        ]
        conn.execute(end_time.insert().values(default_end_time))

        default_accounts = [
            {'name': "錢包", 'balance': 10000, 'category': AccountCategory.CASH.name},
            {'name': "中華郵政", 'balance': 25000, 'category': AccountCategory.DEBIT_CARD.name},
            {'name': "Line Pay", 'balance': 3000, 'category': AccountCategory.ELECTRONIC.name},
            {'name': "Line Pay", 'balance': 100, 'category': AccountCategory.ELECTRONIC.name},
        ]
        conn.execute(account.insert().values(default_accounts))

        default_categories = [
                {'name': "薪資", 'IE': IEDirection.INCOME.name},
                {'name': "獎金", 'IE': IEDirection.INCOME.name},
                {'name': "投資", 'IE': IEDirection.INCOME.name},
                {'name': "保險", 'IE': IEDirection.INCOME.name},
                {'name': "利息", 'IE': IEDirection.INCOME.name},
                {'name': "其它", 'IE': IEDirection.INCOME.name},
                {'name': "食物", 'IE': IEDirection.EXPENSE.name},
                {'name': "飲料", 'IE': IEDirection.EXPENSE.name},
                {'name': "衣服", 'IE': IEDirection.EXPENSE.name},
                {'name': "住宿", 'IE': IEDirection.EXPENSE.name},
                {'name': "交通", 'IE': IEDirection.EXPENSE.name},
                {'name': "其它", 'IE': IEDirection.EXPENSE.name}
            ]
        conn.execute(category.insert().values(default_categories))

        default_locations = [
            {'name': "公司", 'IE': IEDirection.INCOME.name},
            {'name': "學校", 'IE': IEDirection.INCOME.name},
            {'name': "家裡", 'IE': IEDirection.INCOME.name},
            {'name': "政府", 'IE': IEDirection.INCOME.name},
            {'name': "銀行", 'IE': IEDirection.INCOME.name},
            {'name': "其它", 'IE': IEDirection.INCOME.name},
            {'name': "餐廳", 'IE': IEDirection.EXPENSE.name},
            {'name': "飲料店", 'IE': IEDirection.EXPENSE.name},
            {'name': "超商", 'IE': IEDirection.EXPENSE.name},
            {'name': "超市", 'IE': IEDirection.EXPENSE.name},
            {'name': "夜市", 'IE': IEDirection.EXPENSE.name},
            {'name': "文具店", 'IE': IEDirection.EXPENSE.name},
            {'name': "線上商店", 'IE': IEDirection.EXPENSE.name},
            {'name': "百貨公司", 'IE': IEDirection.EXPENSE.name},
            {'name': "學校", 'IE': IEDirection.EXPENSE.name},
            {'name': "其它", 'IE': IEDirection.EXPENSE.name}
        ]
        conn.execute(location.insert().values(default_locations))

        # default_fixedIE = [
        #     {'IE': IEDirection.INCOME.name, 'name': "薪水", 'category': "其他", 'account': "中華郵政", 'amount': 48000, 'location': "其它", 'day': 4, 'note': '', 'registerTime':datetime.today(),'flag': False},
        #     {'IE': IEDirection.INCOME.name, 'name': "獎學金", 'category': "獎金", 'account': "中華郵政", 'amount': 10000, 'location': "其它", 'day': 18, 'note': '', 'registerTime':datetime.today(),'flag': False},
        #     {'IE': IEDirection.EXPENSE.name, 'name': "房租", 'category': "其它", 'account': "其它", 'amount': 6000, 'location': "其它", 'day': 31, 'note': 'sos', 'registerTime':datetime.today(), 'flag': False}
        # ]
        # conn.execute(fixedIE.insert().values(default_fixedIE))

        default_IE_attributes = [
            {'name': "選項A", 'IE': IEDirection.INCOME.name},
            {'name': "選項B", 'IE': IEDirection.EXPENSE.name},
            {'name': "選項C", 'IE': IEDirection.INCOME.name},
        ]
        conn.execute(IEAttribute.insert().values(default_IE_attributes))

        # default_records = [
        #     {'IE': "EXPENSE",'category': "食物", 'account': "現金", 'amount': 50, 'location': "便利商店", 'purchaseDate': '2023-05-01', 'debitDate': '2023-05-01', 'invoice': "12345678", 'note': "milk"},
        #     {'IE': "EXPENSE",'category': "住宿", 'account': "Line Pay", 'amount': 2500, 'location': "其它", 'purchaseDate': datetime.today().date(), 'debitDate': datetime.today().date(), 'invoice': "", 'note': "taipei"},
        #     {'IE': "INCOME",'category': "其它", 'account': "中華郵政", 'amount': 10000, 'location': "其它", 'purchaseDate': '2023-05-22', 'debitDate': '2023-05-23', 'invoice': "19970901", 'note': ""},
        #     {'IE': "EXPENSE",'category': "飲料", 'account': "Line Pay", 'amount': 100, 'location': "飲料店", 'purchaseDate': '2023-05-19', 'debitDate': '2023-05-19', 'invoice': "", 'note': "麻古-芝芝芒果"},
        #     {'IE': "EXPENSE",'category': "飲料", 'account': "現金", 'amount': 101, 'location': "comebuy", 'purchaseDate': '2023-01-01', 'debitDate': '2023-01-01', 'invoice': "", 'note': ""},
        #     {'IE': "EXPENSE",'category': "食物", 'account': "現金", 'amount': 87, 'location': "全家", 'purchaseDate': '2023-02-18', 'debitDate': '2023-02-18','invoice': "", 'note': ""},
        #     {'IE': "EXPENSE",'category': "衣服", 'account': "LinePay", 'amount': 321, 'location': "百貨公司", 'purchaseDate': '2023-03-05', 'debitDate': '2023-03-05','invoice': "", 'note': "洋裝"},
        #     {'IE': "EXPENSE",'category': "食物", 'account': "信用卡", 'amount': 70, 'location': "百貨公司", 'purchaseDate': '2023-03-28', 'debitDate': '2023-03-30','invoice': "", 'note': "coco"}
        # ]
        # conn.execute(record.insert().values(default_records))

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

