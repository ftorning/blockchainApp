from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/<username>')
def profile(username=None):
    if username:
        return render_template("user.html", username=username)
    else:
        return render_template("landing.html")



@app.route('/new')
def new_block():
    return 'new block'


@app.route('/transactions')
def transactions():
    return 'transactions'


@app.route('/transactions/new', methods=['GET', 'POST'])
def new_transaction():
    return 'new transaction'


@app.route('/mine')
def mine_block():
    return '<h1>mine a block</h1>'


if __name__ == '__main__':
    app.run(debug=True)
