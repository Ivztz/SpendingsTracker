from datetime import datetime
from tempfile import mkdtemp
import matplotlib.pyplot as plt

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, connect_db, error_msg, login_required, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


''' -----------------------------------------------------AUTHENTICATION-------------------------------------------'''
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return apology("must provide username")

        # Ensure password was submitted
        elif not password:
            return apology("must provide password")

        # Query database for username
        connection, cursor = connect_db()
        rows = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][-1], password):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]
        flash("Login Successful!")

        connection.close()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username")

        # Ensure password was submitted
        elif not password or not confirmation:
            return apology("must provide password")

        # Check for password requirements
        error = error_msg(password)
        if error:
            return apology(error)

        # Ensure passwords match
        elif password != confirmation:
            return apology("passwords do not match", 403)

        # Query database for username
        connection, cursor = connect_db()
        rows = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()

        # Ensure username not already exists in database
        if len(rows) > 0:
            return apology("username already taken")

        # Hash password
        hash_password = generate_password_hash(password)

        # Insert user into database
        cursor.execute("INSERT INTO users (username, password) VALUES(?, ?)", (username, hash_password))

        # Remember which user has logged in
        user_id = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()[0]
        session["user_id"] = user_id

        # Update database and Close connection
        connection.commit()
        connection.close()

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")

'''-----------------------------------------------Main Page----------------------------------------------------'''

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]

    # Connect to database
    connection, cursor = connect_db()

    # Query for spending summary
    spendings_db = cursor.execute("SELECT category, amount FROM spendings WHERE user_id = ?", (user_id,)).fetchall()

    # Query for budget
    budget = cursor.execute("SELECT budget FROM budgets WHERE user_id = ?", (user_id,)).fetchone()

    # Query for username
    username = cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,)).fetchone()[0]

    if not spendings_db or not budget:
        return render_template("index_empty.html", spendings_db=spendings_db, budget=budget, username=username)

    else:
        spendings_dict = {}
        total = 0

        for spending in spendings_db:
            spendings_dict[spending[0]] = spendings_dict.get(spending[0], 0) + float(spending[1])
            total += float(spending[1])

        remaining = float(budget[0]) - total

        # Pie Chart
        labels = spendings_dict.keys()
        values = spendings_dict.values()
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%')
        plt.savefig(f"./static/summary_{user_id}.png", transparent=True)

        connection.close()

        return render_template("index.html", spendings=spendings_dict, total=total, remaining=remaining, user_id=user_id)


@app.route("/budget", methods=["GET", "POST"])
@login_required
def budget():
    user_id = session["user_id"]

    # Connect to database
    connection, cursor = connect_db()

    # Query for user budget
    budget = cursor.execute("SELECT budget FROM budgets WHERE user_id = ?", (user_id,)).fetchone()

    if request.method == "POST":
        new_budget = request.form.get("budget")
        if not new_budget:
            return apology("Please enter a new budget")
        
        try:
            new_budget = float(new_budget)
        except ValueError:
            return apology("Invalid input")
        
        # Update budget to database
        if budget:
            cursor.execute("UPDATE budgets SET budget = ? WHERE id = ?", (new_budget, user_id))
        else:
            cursor.execute("INSERT INTO budgets (user_id, budget) VALUES(?, ?)", (user_id, new_budget))

        # Update database and Close connection
        connection.commit()
        connection.close()

        flash("Budget Updated Successfully!")

        connection.close()

        # Redirect user to home page
        return redirect("/")

    else:
        if not budget:
            budget = 0
        else:
            budget = budget[0]

        connection.close()
        
        return render_template("budget.html", budget=budget)


@app.route("/add-spending", methods=["GET", "POST"])
@login_required
def spending():
    if request.method == "POST":
        user_id = session["user_id"]

        # Connect to database
        connection, cursor = connect_db()

        spending = request.form.get("spending")
        category = request.form.get("category")

        if not category:
            return apology("Please enter a spending category")
        
        try:
            amount = float(spending)
        except ValueError:
            return apology("Invalid input")
        
        timestamp = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

        # Add spending to database
        cursor.execute("INSERT INTO spendings (user_id, category, amount, timestamp) VALUES(?, ?, ?, ?)", (user_id, category.upper(), amount, timestamp))

        # Update database and Close connection
        connection.commit()
        connection.close()

        flash("New Spendings Added Successfully!")

        connection.close()

        return redirect("/")
    else:
        return render_template("spending.html")


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    user_id = session["user_id"]

    # Connect to database
    connection, cursor = connect_db()

    if request.method == "POST":
        spendings_id = int(request.form.get("delete"))
        cursor.execute("DELETE FROM spendings WHERE id = ?", (spendings_id,))
        connection.commit()

        flash("Spending History Deleted!")

    # Query for spending summary
    spendings_db = cursor.execute("SELECT id, category, amount, timestamp FROM spendings WHERE user_id = ?", (user_id,)).fetchall()
    connection.close()

    return render_template("/history.html", spendings=spendings_db)


if __name__ == '__main__':
    app.run(debug=True)