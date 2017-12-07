from flask import Flask, request, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Chain, Block, User, Transaction, connect_string
import os


app = Flask(__name__)

# connect to the database
engine = create_engine('sqlite:///blockchain.db')
Base.metadata.bind = engine

# create session
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/<int:user_id>/')
@app.route('/<int:user_id>/home/')
def authenticate(user_id=None):
    print('id = {}'.format(user_id))
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
        greeting = 'Welcome {}!'.format(user.fname)
        return greeting
    else:
        return render_template("landing.html")


@app.route('/<user_id>/profile/')
def profile(user_id=None):
    return user_id
    # if user_id:


@app.route('/new/')
def new_block():
    return 'new block'


@app.route('/transactions/')
def transactions():
    transactions_list = session.query(Transaction).all()
    output = ''
    for t in transactions_list:
        output += t.sender.email
        output += '<br>'

    return output


@app.route('/transactions/new/', methods=['GET', 'POST'])
def new_transaction():
    return 'new transaction'


@app.route('/mine/')
def mine_block():
    return '<h1>mine a block</h1>'


if __name__ == '__main__':
    app.run(debug=True)
