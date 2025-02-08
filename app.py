from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import exc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense_tracker.db'
app.config['SECRET_KEY'] = 'mysecretkey'

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # <-- Initialize Migrate

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    income = db.Column(db.Float, nullable=False)
    expense_limit = db.Column(db.Float, nullable=False)
    expenses = db.relationship('Expense', backref='user', lazy=True)

    @property
    def total_expenses(self):
        # Calculate total expenses by summing up the amounts of each associated expense
        return sum(expense.amount for expense in self.expenses)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    users = User.query.all()
    return render_template('dashboard.html', users=users)

# Add User route
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        income = float(request.form['income'])
        expense_limit = float(request.form['expense_limit'])

        # Create a new user
        new_user = User(name=name, income=income, expense_limit=expense_limit)
        db.session.add(new_user)
        db.session.commit()

        flash('User added successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_user.html')

# Delete all users route
@app.route('/delete_all_users', methods=['POST'])
def delete_all_users():
    try:
        # Delete all users and their expenses
        db.session.query(User).delete()
        db.session.query(Expense).delete()
        db.session.commit()

        flash('All users and expenses have been deleted.', 'danger')
        return redirect(url_for('dashboard'))

    except exc.SQLAlchemyError as e:
        db.session.rollback()
        flash('An error occurred while deleting users.', 'danger')
        return redirect(url_for('dashboard'))

# Delete individual user route
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    try:
        # Delete user and their expenses
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        flash(f'User {user.name} has been deleted.', 'danger')
        return redirect(url_for('dashboard'))

    except exc.SQLAlchemyError as e:
        db.session.rollback()
        flash('An error occurred while deleting the user.', 'danger')
        return redirect(url_for('dashboard'))

# Add Expense route
@app.route('/add_expenses/<int:user_id>', methods=['GET', 'POST'])
def add_expenses(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        expense_name = request.form['expense_name']
        amount = float(request.form['amount'])

        # Check if expense exceeds limit
        total_expenses = sum([expense.amount for expense in user.expenses])
        if total_expenses + amount > user.expense_limit:
            flash('Expense exceeds the user\'s limit!', 'warning')
        else:
            # Create and save expense
            expense = Expense(name=expense_name, amount=amount, user_id=user.id)
            db.session.add(expense)
            db.session.commit()
            flash(f'Expense "{expense_name}" added successfully.', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_expenses.html', user=user)


# View Expenses route
@app.route('/view_expenses/<int:user_id>')
def view_expenses(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('view_expenses.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
