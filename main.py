from flask import Flask, request, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Block, User, Transaction, connect_string
import os


app = Flask(__name__)

# connect to the database
engine = create_engine('sqlite:///blockchain.db')
Base.metadata.bind = engine

# create session
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/', methods=['GET'])
@app.route('/<int:user_id>/', methods=['GET'])
@app.route('/<int:user_id>/home/', methods=['GET'])
def home(user_id=None):
    print('id = {}'.format(user_id))
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
        return render_template("home.html", user=user)
    else:
        return render_template("landing.html")


@app.route('/create_account/', methods=['GET', 'POST'])
def create_user():
    return None


@app.route('/sign_in/', methods=['GET', 'POST'])
def sign_in():
    return None


@app.route('/<user_id>/profile/', methods=['GET'])
def profile(user_id=None):
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
        pending = session.query(Transaction) \
            .filter((Transaction.block_id.proof == 0) &
                    ((Transaction.sender_id == user_id) |
                     (Transaction.recipient_id == user_id)))

        return render_template("profile.html", user=user, pending=pending)
    else:
        return render_template("landing.html")


@app.route('/<user_id>/profile/edit/', methods=['GET', 'POST'])
def edit_profile(user_id=None):
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
        return render_template("profile_edit.html", user=user)
    else:
        return render_template("landing.html")


@app.route('/<user_id>/transactions/', methods=['GET'])
def transactions(user_id=None):
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
        transactions_list = session.query(Transaction.recipient).all()
        return render_template("transactions.html", user=user)
    else:
        return render_template("landing.html")


@app.route('/<user_id>/transactions/new/', methods=['GET', 'POST'])
def new_transaction(user_id=None):
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
        # transactions_list = session.query(Transaction.recipient).all()
        return render_template("transactions.html", user=user)
    else:
        return render_template("landing.html")


@app.route('/<user_id>/mine/', methods=['GET', 'POST'])
def mine_block(user_id=None):
    return '<h1>mine a block</h1>'


@app.route('/<user_id>/summary/', methods=['GET', 'POST'])
def chain_summary(user_id=None):
    return '<h1>summary page</h1>'


@app.route('/<user_id>/summary/block_id/', methods=['GET', 'POST'])
def block_summary(user_id=None, block_id=None):
    return '<h1>summary page</h1>'


if __name__ == '__main__':
    app.run(debug=True)
