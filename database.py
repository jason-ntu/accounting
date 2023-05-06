import const
import mysqlConfig as cfg
import sqlalchemy as sql
from sqlalchemy_utils import database_exists, create_database

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
                           'amount', sql.Float(), nullable=False)
                       )
    metadata.create_all(engine)
    
    conn.execute(budget.insert().values(id=1, amount=0))
    conn.commit()

if __name__ == "__main__":
    initialize(cfg.dev)
