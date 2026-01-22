from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Instead of connecting via db driver like
# conn = psycopg.connect(
#     dbname=getenv('DB_NAME'), user=getenv('DB_USER'), password=getenv('DB_PASS'), row_factory=dict_row
# )
# create a database URL like
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-addr (or) hostname>/<dbname>'

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()