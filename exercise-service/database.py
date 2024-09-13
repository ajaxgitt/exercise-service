from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#  mysql+mysqldb://root:password@mysql:3307/problems
SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://root:password@mysql:3306/problems"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

