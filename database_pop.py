from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Chain, Block, Transaction, User
from datetime import datetime


engine = create_engine('sqlite:///blockchain.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# create a chain

chain = Chain(timestamp=datetime.now())

session.add(chain)

# create an initial block

block = Block(index=1, timestamp=datetime.now(), proof=100, previous_hash=1, chain_id=1)

session.add(block)

# create users and an admin account for mining rewards

admin_account = User(email='None', fname='Admin', lname='Blockchain')
user1 = User(email='ftorning@gmail.com', fname='Fraser', lname='Torning')
user2 = User(email='stephaniekaczmarski@gmail.com', fname='Stephanie', lname='Kaczmarski')

session.add(admin_account)
session.add(user1)
session.add(user2)

# create transactions

tx1 = Transaction(amount=2, timestamp=datetime.now(), block_id=1, sender_id=1, recipient_id=2)
tx2 = Transaction(amount=3, timestamp=datetime.now(), block_id=1, sender_id=2, recipient_id=1)

session.add(tx1)
session.add(tx2)

session.commit()
