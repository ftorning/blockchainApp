import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine





Base = declarative_base()


def connect_string():
    return 'sqlite:///blockchain.db'

# for testing only
# from sqlalchemy_utils.functions import database_exists, drop_database
# if database_exists(connect_string()):
#     drop_database(connect_string())


# initial chain instantiated by database_pop
class Chain(Base):

    __tablename__ = 'chain'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)


class Block(Base):

    __tablename__ = 'block'

    id = Column(Integer, primary_key=True, autoincrement=True)
    index = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    proof = Column(Integer, nullable=False)
    previous_hash = Column(String(80), nullable=False)
    chain_id = Column(Integer, ForeignKey('chain.id'))
    chain = relationship(Chain)


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(80), nullable=False, unique=True)
    fname = Column(String(80), nullable=False)
    lname = Column(String(80), nullable=False)
    balance = Column(Float, nullable=False)
    picture = Column(String(120))
    password = Column(String(120), nullable=False)


class Transaction(Base):

    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    block_id = Column(Integer, ForeignKey('block.id'))
    sender_email = Column(String(80), ForeignKey('user.email'))
    recipient_email = Column(String(80), ForeignKey('user.email'))
    block = relationship(Block)
    sender = relationship(User, foreign_keys=[sender_email])
    recipient = relationship(User, foreign_keys=[recipient_email])


engine = create_engine(connect_string())
Base.metadata.create_all(engine)
