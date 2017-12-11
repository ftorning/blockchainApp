from flask import Flask, request, render_template, redirect, url_for, flash
from sqlalchemy import create_engine, and_, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Block, User, Transaction, connect_string
from datetime import datetime
import blockchain


app = Flask(__name__)
app.secret_key = 'my secret key'

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
    user = User()
    if request.method == 'POST':
        if request.form['fname']:
            user.fname = request.form['fname']
        if request.form['lname']:
            user.lname = request.form['lname']
        if request.form['email']:
            user.email = request.form['email']
        if request.form['password']:
            user.password = request.form['password']
        if request.form['add_funds']:
            user.balance = request.form['add_funds']
        user.picture = 'https://s3.amazonaws.com/blockchainproject/anonymous-512.png'
        session.add(user)
        session.commit()
        return redirect(url_for('profile', user_id=user.id))
    else:
        return render_template("create_account.html")


@app.route('/sign_in/', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        print(request.form)
        if request.form['email']:
            try:
                user = session.query(User).filter_by(email=request.form['email']).one()
            except:
                flash('Invalid credentials, please try again')
                return render_template("sign_in.html")
            if user.password == request.form['password']:
                flash('Welcome back {}!'.format(user.fname))
                return redirect(url_for('home', user_id=user.id))
            else:
                flash('Invalid credentials, please try again')
                return render_template("sign_in.html")
        else:
            flash('Please enter your email and password')
            return render_template("sign_in.html")
    else:
        return render_template("sign_in.html")


@app.route('/<user_id>/profile/', methods=['GET'])
def profile(user_id=None):
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
        pending = session.query(Transaction, Block) \
            .filter((Block.proof == 0) &
                    ((Transaction.sender_email == user.email) |
                     (Transaction.recipient_email == user.email)))

        return render_template("profile.html", user=user, pending=pending)
    else:
        return render_template("landing.html")


@app.route('/<user_id>/profile/edit/', methods=['GET', 'POST'])
def edit_profile(user_id=None):
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
        if request.method == 'POST':
            if request.form['fname']:
                user.fname = request.form['fname']
            if request.form['lname']:
                user.lname = request.form['lname']
            if request.form['email']:
                user.email = request.form['email']
            if request.form['password']:
                user.password = request.form['password']
            session.add(user)
            session.commit()
            return redirect(url_for('profile', user_id=user.id))
        else:
            return render_template("profile_edit.html", user=user)
    else:
        return render_template("landing.html")


@app.route('/<user_id>/profile/add_funds/', methods=['GET', 'POST'])
def add_funds(user_id=None):
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
        if request.method == 'POST':
            if request.form['amount']:
                user.balance += float(request.form['amount'])
            else:
                flash('Please enter the amount of funds to add')
                return redirect(url_for('add_funds', user_id=user.id))
            session.add(user)
            session.commit()
            flash('Funds successfully added!')
            return redirect(url_for('profile', user_id=user.id))
        else:
            return render_template('add_funds.html', user=user)
    else:
        return render_template("landing.html")


@app.route('/<user_id>/profile/delete/', methods=['GET', 'POST'])
def delete_profile(user_id=None):
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
        if request.method == 'POST':
            session.delete(user)
            session.commit()
            flash('User Deleted')
            return redirect(url_for('home', user_id=None))
        else:
            return render_template("profile_delete.html", user=user)
    else:
        return render_template("landing.html")


@app.route('/<user_id>/transactions/', methods=['GET'])
def transactions(user_id=None):
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
        tx_in = session.query(Transaction).filter(Transaction.recipient_email == user.email)
        tx_out = session.query(Transaction).filter(Transaction.sender_email == user.email)
        return render_template("transactions.html", user=user, tx_in=tx_in, tx_out=tx_out)
    else:
        return render_template("landing.html")


@app.route('/<user_id>/transactions/new/', methods=['GET', 'POST'])
def new_transaction(user_id=None):
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
        rec_list = session.query(User).filter((User.id > 1) & (User.id != user.id)).all()
        block = session.query(func.max(Block.id)).one()
        print(block)
        if request.method == 'POST':
            tx = Transaction()
            if request.form['recipient']:
                tx.recipient_email = request.form['recipient']
            if request.form['amount'] and float(request.form['amount']) <= user.balance:
                tx.amount = float(request.form['amount'])
            else:
                flash('Insufficient funds')
                return render_template("new_transaction.html", user=user, rec_list=rec_list, block=block)
            tx.block_id = block[0]
            tx.sender_email = user.email
            tx.timestamp = datetime.now()
            user.balance = user.balance - tx.amount
            session.add(tx)
            session.add(user)
            session.commit()
            flash('Transaction successful!')
            return redirect(url_for('home', user_id=user.id))
        return render_template("new_transaction.html", user=user, rec_list=rec_list, block=block)
    else:
        return render_template("landing.html")


@app.route('/<user_id>/mine/', methods=['GET', 'POST'])
def mine(user_id=None):
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
        block_id = session.query(func.max(Block.id)).one()
        block = session.query(Block).filter(Block.id == block_id[0]).one()
        txs = session.query(Transaction).filter(Transaction.block_id == block_id[0]).all()
        tx_cnt = len(txs)
        return render_template("mine.html", user=user, block=block, txs=txs, tx_cnt=tx_cnt)
    else:
        return render_template("landing.html")


@app.route('/<user_id>/mine/<block_id>', methods=['GET', 'POST'])
def mine_block(user_id=None, block_id=None):
    if user_id and block_id:
        user = session.query(User).filter_by(id=user_id).one()
        block = session.query(Block).filter_by(id=block_id).one()
        new_blk = Block()
        new_blk.index = int(block.index) + 1
        new_blk.timestamp = datetime.now()
        new_blk.proof = blockchain.proof_of_work(block.proof)
        new_blk.previous_hash = blockchain.hash_block(block)
        new_blk.chain_id = block.chain_id
        session.add(new_blk)
        session.commit()

        miner_tx = Transaction()
        miner_tx.amount = 100
        miner_tx.timestamp = datetime.now()
        miner_tx.block_id = new_blk.id
        miner_tx.sender_email = 'Mine Reward'
        miner_tx.recipient_email = user.email
        session.add(miner_tx)
        session.commit()

        flash('Mining Successful!')
        return redirect(url_for('mine', user_id=user.id))
    else:
        return render_template("landing.html")


# @staticmethod
# def valid_proof(last_proof, proof):
#     guess = f'{last_proof}{proof}'.encode()
#     guess_hash = hashlib.sha256(guess).hexdigest()
#     return guess_hash[:4] == "0000"
#
#
# def proof_of_work(last_proof):
#     proof = 0
#     while valid_proof(last_proof, proof) is False:
#         proof += 1
#     return proof
#
#
# def _hash(block):
#     block_string = json.dumps(block, sort_keys=True).encode()
#     return hashlib.sha256(block_string).hexdigest()

# def mine(user_id):
#     last_block = blockchain.last_block
#     last_proof = last_block['proof']
#     proof = blockchain.proof_of_work(last_proof)
#
#     # reward the miner
#     blockchain.new_transaction(
#         sender="0",
#         recipient=node_identifier,
#         amount=1,
#     )
#
#     # add new block to the chain
#     previous_hash = blockchain.hash(last_block)
#     block = blockchain.new_block(proof, previous_hash)
#
#
# def new_block(proof, previous_hash=None):
#
#     block = {
#         'index': len(self.chain) + 1,
#         'timestamp': time(),
#         'transactions': self.current_transactions,
#         'proof': proof,
#         'previous_hash': previous_hash or self.hash(self.chain[-1])
#     }
#
#     # reset transaction list
#     self.current_transactions = []
#
#     # append new block to chain
#     self.chain.append(block)
#
#     return block


if __name__ == '__main__':
    app.run(debug=True)
