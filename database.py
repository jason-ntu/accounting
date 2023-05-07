import const
import mysqlConfig as cfg
import sqlalchemy as sql
from sqlalchemy_utils import database_exists, create_database, drop_database
from payment import PaymentCategory


def initialize(config):
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

    metadata.create_all(engine)
    
    conn.execute(budget.insert().values(id=1, amount=0))
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
