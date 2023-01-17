from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT, SMALLINT, MONEY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Currency(Base):
    __tablename__ = "currencies"

    id = Column(TEXT, primary_key=True)
    num_code = Column(TEXT, nullable=False)
    char_code = Column(TEXT, nullable=False)
    nominal = Column(SMALLINT, nullable=False)
    name = Column(TEXT, nullable=False)
    value = Column(MONEY, nullable=False)
    previous = Column(MONEY, nullable=False)
