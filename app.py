import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLite database
db = SQL("sqlite:///minux.db")

ACCOUNT = 150000

@app.route("/")
@login_required
def index():
    now = datetime.now()

    latest_transactions = db.execute("SELECT transactions.type, transactions.amount, categories.name, \
                                      transactions.description, transactions.transacted_on FROM transactions \
                                      JOIN categories ON transactions.category_id = categories.category_id \
                                      WHERE transactions.user_id IN (SELECT id FROM users WHERE id = ?) \
                                      ORDER BY CAST(strftime('%Y', transacted_on) AS INT) DESC, \
                                      CAST(strftime('%m', transacted_on) AS INT) DESC, \
                                      CAST(strftime('%d', transacted_on) AS INT) DESC, \
                                      transactions.transaction_id DESC LIMIT 4", session['user_id'])

    for transaction in latest_transactions:
        transaction['transacted_on'] = datetime.strptime(transaction['transacted_on'], ('%Y-%m-%d')).strftime('%d %b')

    expenses = db.execute("SELECT amount FROM transactions WHERE user_id IN (SELECT id FROM users WHERE id = ?) \
                           AND type = ? AND CAST(strftime('%Y', transacted_on) AS INT) = ? AND \
                           CAST(strftime('%m', transacted_on) AS INT) = ?", session['user_id'], "expense", now.year, now.month)

    month_name = now.strftime('%B')
    month_expense = 0

    for expense in expenses:
        month_expense += expense['amount']

    # Render the home (index) page
    return render_template("index.html", month=month_name, expense=f'{month_expense:,.2f}', transactions=latest_transactions)


@app.route("/log")
@login_required
def log():
    return render_template("log.html")


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/edit-transaction")
@login_required
def edit_transaction():
    return render_template("edit-transaction.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return apology("Must provide password", 403)

        # Ensure password was submitted
        if not password:
            return apology("Must provide password", 403)

        # Query database for username
        users = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(users) != 1 or not check_password_hash(users[0]['hash'], password):
            return apology("Invalid credentials", 403)

        # Remember which user has logged in
        session['user_id'] = users[0]['id']

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()
    return redirect("/")


@app.route("/signup", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Ensure all required data was submitted
        if not firstname:
            return apology("Must provide first name", 400)

        if not username:
            return apology("Must provide username", 400)

        if not password or not confirm_password:
            return apology("Must provide both passwords", 400)

        if password != confirm_password:
            return apology("Passwords not same", 400)

        # Username already exists
        username_exists = db.execute("SELECT id FROM users WHERE username = ?", username)
        if username_exists:
            return apology("Username already exists", 400)

        # Generate a password hash to store
        pw_hash = generate_password_hash(password)

        # Insert user into database
        db.execute("INSERT INTO users (firstname, lastname, username, hash) VALUES (?, ?, ?, ?)", firstname, lastname, username, pw_hash)

        # Remember which user has logged in
        user = db.execute("SELECT id FROM users WHERE username = ?", username)
        session['user_id'] = user[0]['id']

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/expense", methods=["GET", "POST"])
@login_required
def expense():
    """Add expense"""

    type = "expense"
    categories = db.execute("SELECT category_id, name FROM categories WHERE transaction_type = ?", type)

    if request.method == "POST":
        amount = request.form.get("amount")
        category = request.form.get("category")
        category_id = -1
        description = request.form.get("description")
        transacted_on = request.form.get("transacted_on")

        if not amount:
            return apology(f"Must provide {type.capitalize()} amount", 400)

        for c in categories:
            if category.lower() == c['name'].lower():
                category_id = c['category_id']

        if not category or category_id == -1:
            return apology("Must select a valid category", 400)

        # Insert expense into database
        db.execute("INSERT INTO transactions (user_id, type, amount, category_id, description, created_on, created_on_utc, transacted_on) \
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)", session['user_id'], type, amount, category_id, description, datetime.now(), datetime.utcnow(), transacted_on)

        return redirect("/")

    else:
        return render_template("expense.html", categories=categories)


@app.route("/income", methods=["GET", "POST"])
@login_required
def income():
    """Add income"""

    type = "income"
    categories = db.execute("SELECT category_id, name FROM categories WHERE transaction_type = ?", type)

    if request.method == "POST":
        amount = request.form.get("amount")
        category = request.form.get("category")
        category_id = -1
        description = request.form.get("description")
        transacted_on = request.form.get("transacted_on")

        if not amount:
            return apology(f"Must provide {type.capitalize()} amount", 400)

        for c in categories:
            if category.lower() == c['name'].lower():
                category_id = c['category_id']

        if not category or category_id == -1:
            return apology("Must select a valid category", 400)

        # Insert expense into database
        db.execute("INSERT INTO transactions (user_id, type, amount, category_id, description, created_on, created_on_utc, transacted_on) \
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)", session['user_id'], type, amount, category_id, description, datetime.now(), datetime.utcnow(), transacted_on)

        return redirect("/") 

    else:
        return render_template("income.html", categories=categories)