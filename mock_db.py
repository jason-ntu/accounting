from unittest import TestCase
import mysqlConfig as cfg
import sqlalchemy as sql
from mock import patch
import const
from payment import PaymentCategory
from fixedIE import FixedIEType, CategoryOption, PaymentOption
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

        payment = sql.Table('Payment', metadata,
                         sql.Column(
                             'id', sql.Integer(), nullable=False, primary_key=True),
                         sql.Column(
                             'name', sql.String(50), nullable=False),
                         sql.Column(
                             'balance', sql.Float(), nullable=False),
                         sql.Column(
                             'category', sql.Enum(PaymentCategory), default=PaymentCategory.CASH, nullable=False)
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
                            'payment', sql.String(30), nullable=False),
                        sql.Column(
                            'amount', sql.Float(), nullable=False),
                        sql.Column(
                            'day', sql.Integer(), nullable=False),
                        sql.Column(
                            'note', sql.String(30), nullable=True),
                        sql.Column(
                            'flag', sql.Boolean(), default=False, nullable=False)
        )

        record = sql.Table('Record', metadata,
                        sql.Column('id', sql.Integer(), nullable=False, primary_key=True),
                        sql.Column('category', sql.String(30), nullable=False),
                        sql.Column('payment', sql.String(30), nullable=False),
                        sql.Column('amount', sql.Integer(), nullable=False),
                        sql.Column('place', sql.String(30), nullable=False),
                        sql.Column('time', sql.Date(), default=datetime.today(), nullable=False)
        )

        metadata.create_all(engine)

        conn.execute(budget.insert().values(id=1, amount=10000.00))

        default_payments = [
            {'name': "錢包", 'balance': 10000, 'category': PaymentCategory.CASH.name},
            {'name': "中華郵政", 'balance': 25000, 'category': PaymentCategory.DEBIT_CARD.name},
            {'name': "Line Pay", 'balance': 3000, 'category': PaymentCategory.ELECTRONIC.name},
            {'name': "Line Pay", 'balance': 100, 'category': PaymentCategory.ELECTRONIC.name},
        ]
        conn.execute(payment.insert().values(default_payments))

        default_incomes = [
            {'name': "獎金"},
            {'name': "退款"},
            {'name': "回饋"},
            {'name': "其他"}
        ]
        conn.execute(income.insert().values(default_incomes))

        default_fixedIE = [
            {'IE': FixedIEType.INCOME.name, 'name': "獎學金", 'category': CategoryOption.OTHER.name, 'payment': PaymentOption.OTHER.name, 'amount': 10000, 'day': 15, 'note': '', 'flag': True},
            {'IE': FixedIEType.EXPENSE.name, 'name': "房租", 'category': CategoryOption.OTHER.name, 'payment': PaymentOption.OTHER.name, 'amount': 6000, 'day': 20, 'note': 'sos', 'flag': False}
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
            {'category': "FOOD", 'payment': "現金", 'amount': 50, 'place': "7-11", 'time': '2023-05-01'},
            {'category': "BEVERAGE", 'payment': "現金", 'amount': 101, 'place': "comebuy", 'time': '2023-01-01'},
            {'category': "FOOD", 'payment': "現金", 'amount': 87, 'place': "全家", 'time': '2023-02-18'},
            {'category': "FOOD", 'payment': "信用卡", 'amount': 321, 'place': "subway", 'time': '2023-04-03'},
            {'category': "BEVERAGE", 'payment': "電子支付", 'amount': 70, 'place': "milksha", 'time': '2023-02-02'}
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

