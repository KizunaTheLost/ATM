from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atm.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, nullable=False)

# Create the database and the db table
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        account_number = request.form['account_number']
        username = request.form['username']
        initial_deposit = float(request.form['initial_deposit'])
        
        new_account = Account(account_number=account_number, username=username, balance=initial_deposit)
        db.session.add(new_account)
        db.session.commit()
        
        flash('Account created successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('create_account.html')

@app.route('/view_balance', methods=['GET', 'POST'])
def view_balance():
    account = None
    if request.method == 'POST':
        account_number = request.form['account_number']
        account = Account.query.filter_by(account_number=account_number).first()
        
        if not account:
            flash('Account not found!', 'danger')
    
    return render_template('view_balance.html', account=account)

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        account_number = request.form['account_number']
        amount = float(request.form['amount'])
        
        account = Account.query.filter_by(account_number=account_number).first()
        if account:
            account.balance += amount
            db.session.commit()
            flash('Deposit successful!', 'success')
        else:
            flash('Account not found!', 'danger')
    
    return render_template('deposit.html')

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'POST':
        account_number = request.form['account_number']
        amount = float(request.form['amount'])
        
        account = Account.query.filter_by(account_number=account_number).first()
        if account:
            if account.balance >= amount:
                account.balance -= amount
                db.session.commit()
                flash('Withdrawal successful!', 'success')
            else:
                flash('Insufficient funds!', 'danger')
        else:
            flash('Account not found!', 'danger')
    
    return render_template('withdraw.html')

@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    if request.method == 'POST':
        account_number = request.form['account_number']
        account = Account.query.filter_by(account_number=account_number).first()
        
        if account:
            db.session.delete(account)
            db.session.commit()
            flash('Account deleted successfully!', 'success')
        else:
            flash('Account not found!', 'danger')
    
    return render_template('delete_account.html')

if __name__ == '__main__':
    app.run(debug=True)
