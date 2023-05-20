import const
import mysqlConfig as cfg
import sqlalchemy as sql
from sqlalchemy_utils import database_exists, create_database, drop_database
from payment import PaymentCategory
from fixedIE import FixedIECategory
from datetime import datetime


def initialize(config):
    print("Initialize database...")

    if not database_exists(config['url']):
        create_database(config['url'])
        print("%sDatabase %s created.%s" %
              (const.ANSI_BLACK, config['database'], const.ANSI_RESET))
    else:
        print("%sDatabase %s already exist.%s" %
              (const.ANSI_BLACK, config['database'], const.ANSI_RESET))

    engine = sql.create_engine(config['url'])
    conn = engine.connect()
    metadata = sql.MetaData()

    budget = sql.Table('Budget', metadata,
                        sql.Column(
                            'id', sql.Integer(), nullable=False, primary_key=True),
                        sql.Column(
                            'amount', sql.Float(), default=0, nullable=False)
                       )

    payment = sql.Table('Payment', metadata,
                        sql.Column(
                            'id', sql.Integer(), nullable=False, primary_key=True),
                        sql.Column(
                            'name', sql.String(30), nullable=False),
                        sql.Column(
                            'balance', sql.Float(), default=0, nullable=False),
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
                        sql.Column('id', sql.Integer(),
                                nullable=False, primary_key=True),
                        sql.Column('name', sql.String(50), nullable=False),
                        sql.Column('amount', sql.Float(), nullable=False),
                        sql.Column('category', sql.Enum(
                            FixedIECategory), nullable=False)
                        )

    record = sql.Table('Record', metadata,
                        sql.Column(
                            'id', sql.Integer(), nullable=False, primary_key=True),
                        sql.Column(
                            'category', sql.String(30), nullable=False),
                        sql.Column(
                            'payment', sql.String(30), nullable=False),
                        sql.Column(
                            'amount', sql.Integer(), nullable=False),
                        sql.Column(
                            'place', sql.String(30), nullable=False),
                        sql.Column(
                            'time', sql.Date(), default=datetime.today(), nullable=False)
                        )

    metadata.create_all(engine)

    conn.execute(budget.insert().values(id=1, amount=0))

    default_payments = [
        {'name': "錢包", 'balance': 0,
         'category': PaymentCategory.CASH.name},
        {'name': "儲蓄卡", 'balance': 25000,
         'category': PaymentCategory.DEBIT_CARD.name},
        {'name': "信用卡", 'balance': 3000,
         'category': PaymentCategory.CREDIT_CARD.name},
        {'name': "Line Pay", 'balance': 100,
         'category': PaymentCategory.ELECTRONIC.name},
        {'name': "Metamask", 'balance': 100,
         'category': PaymentCategory.OTHER.name},
    ]
    conn.execute(payment.insert().values(default_payments))

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
        {'name': "餐廳"},
        {'name': "飲料店"},
        {'name': "超商"},
        {'name': "超市"},
        {'name': "夜市"},
        {'name': "文具店"},
        {'name': "線上商店"},
        {'name': "百貨公司"},
        {'name': "學校"},
        {'name': "其它"}
    ]
    conn.execute(location.insert().values(default_locations))

    conn.commit()

# Remove originals records and intialize again
def reinitialize(config):
    if database_exists(config['url']):
        drop_database(config['url'])
        print("%sOriginal dDatabase %s dropped.%s" %
              (const.ANSI_BLACK, config['database'], const.ANSI_RESET))
    initialize(config)

if __name__ == "__main__":
    # initialize(cfg.dev)
    reinitialize(cfg.dev)
