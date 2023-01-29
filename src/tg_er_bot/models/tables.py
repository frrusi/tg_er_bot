from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT, SMALLINT, INTEGER, BOOLEAN, FLOAT
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class BaseModel(base):  # TODO
    __abstract__ = True

    # def get_columns(self):
    #     return self.__mapper__.attrs.keys()
    #
    # def get_columns_names(self):
    #     return [column.split('_', 1)[-1] for column in self.get_columns()]
    #
    # def get_columns_object(self):
    #     return [attrgetter(column)(self.__class__) for column in self.get_columns()]


class Currency(base):
    __tablename__ = "currencies"

    ID = Column(TEXT, primary_key=True)
    NumCode = Column(TEXT, nullable=False)
    CharCode = Column(TEXT, nullable=False)
    Nominal = Column(SMALLINT, nullable=False)
    Name = Column(TEXT, nullable=False)
    Value = Column(FLOAT, nullable=False)
    Previous = Column(FLOAT, nullable=False)


class User(base):
    __tablename__ = "users"

    id = Column(INTEGER, primary_key=True)
    is_bot = Column(BOOLEAN, nullable=False)
    is_admin = Column(BOOLEAN, default=False, nullable=False)
    is_creator = Column(BOOLEAN, default=False, nullable=False)
    is_blocked = Column(BOOLEAN, default=False, nullable=False)
    first_name = Column(TEXT)
    last_name = Column(TEXT)
    username = Column(TEXT, nullable=False, unique=True)
    language_code = Column(TEXT)
    is_premium = Column(BOOLEAN)
    added_to_attachment_menu = Column(BOOLEAN)
    can_join_groups = Column(BOOLEAN)
    can_read_all_group_messages = Column(BOOLEAN)
    supports_inline_queries = Column(BOOLEAN)
