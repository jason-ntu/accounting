from unittest import TestCase
import mysqlConfig as cfg
import sqlalchemy as sql
from mock import patch
import const
from payment import PaymentCategory
from income import FixedIECategory
from sqlalchemy_utils import database_exists, create_database, drop_database

class MockDB(TestCase):

    config = cfg.test

    @classmethod
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

        fixedIE = sql.Table('FixedIE', metadata,
                        sql.Column('id', sql.Integer(), nullable=False, primary_key=True),
                        sql.Column('name', sql.String(50), nullable=False),
                        sql.Column('amount', sql.Float(), nullable=False),
                        sql.Column('category', sql.Enum(FixedIECategory), nullable=False)
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

