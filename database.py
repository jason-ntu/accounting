import const
import mysqlConfig as cfg
import sqlalchemy as sql
from sqlalchemy_utils import database_exists, create_database, drop_database
from account import AccountCategory
from recordDirection import IEDirection
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

    metadata.create_all(engine)

    default_end_time = [
        {'time': datetime(1970, 1, 1, 0, 0, 0)}
    ]
    conn.execute(end_time.insert().values(default_end_time))


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
