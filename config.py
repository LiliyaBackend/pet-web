from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

db_config = {
    'user': 'root',
    'host': 'localhost',
    'database': 'math_calc'
}

sql_engine = create_engine(f"mysql+pymysql://{db_config['user']}:@{db_config['host']}/{db_config['database']}",
                           echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sql_engine)
