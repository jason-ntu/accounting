import const
import mysqlConfig as cfg
import sqlalchemy as sql
from sqlalchemy_utils import database_exists, create_database, drop_database
from account import AccountCategory
from fixedIE import FixedIEType
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
                            'amount', sql.Float(), default=0, nullable=False)
                       )

    account = sql.Table('Account', metadata,
                        sql.Column(
                            'id', sql.Integer(), nullable=False, primary_key=True),
                        sql.Column(
                            'name', sql.String(30), nullable=False),
                        sql.Column(
                            'balance', sql.Float(), default=0, nullable=False),
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
                            'name', sql.String(50), nullable=False),
                        sql.Column(
                            'IE', sql.Enum(FixedIEType), nullable=False)
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

    conn.execute(budget.insert().values(id=1, amount=0))

    default_accounts = [
        {'name': "錢包", 'balance': 0,
         'category': AccountCategory.CASH.name},
        {'name': "儲蓄卡", 'balance': 25000,
         'category': AccountCategory.DEBIT_CARD.name},
        {'name': "信用卡", 'balance': 3000,
         'category': AccountCategory.CREDIT_CARD.name},
        {'name': "Line Pay", 'balance': 100,
         'category': AccountCategory.ELECTRONIC.name},
        {'name': "Metamask", 'balance': 100,
         'category': AccountCategory.OTHER.name},
    ]
    conn.execute(account.insert().values(default_accounts))

    default_categories = [
        {'name': "薪資", 'IE': FixedIEType.INCOME.name},
        {'name': "獎金", 'IE': FixedIEType.INCOME.name},
        {'name': "投資", 'IE': FixedIEType.INCOME.name},
        {'name': "保險", 'IE': FixedIEType.INCOME.name},
        {'name': "利息", 'IE': FixedIEType.INCOME.name},
        {'name': "其它", 'IE': FixedIEType.INCOME.name},
        {'name': "食物", 'IE': FixedIEType.EXPENSE.name},
        {'name': "飲料", 'IE': FixedIEType.EXPENSE.name},
        {'name': "衣服", 'IE': FixedIEType.EXPENSE.name},
        {'name': "住宿", 'IE': FixedIEType.EXPENSE.name},
        {'name': "交通", 'IE': FixedIEType.EXPENSE.name},
        {'name': "其它", 'IE': FixedIEType.EXPENSE.name}
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
