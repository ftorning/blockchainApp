import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


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


class Transaction(Base):

    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    block_id = Column(Integer, ForeignKey('block.id'))
    sender_id = Column(Integer, ForeignKey('user.id'))
    recipient_id = Column(Integer, ForeignKey('user.id'))
    block = relationship(Block)
    sender = relationship("User", foreign_keys=[sender_id])
    recipient = relationship(User, foreign_keys=[recipient_id])


engine = create_engine('sqlite:///blockchain.db')

Base.metadata.create_all(engine)
