import csv
import datetime
import subprocess
import urllib
import uuid
import sqlite3

from flask import redirect, render_template, session
from functools import wraps

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def connect_db():
    connection = sqlite3.connect("spendings.db")
    cursor = connection.cursor()
    return connection, cursor


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def error_msg(password):
    # Password length check
    if len(password) < 6:
        return "Password must contain at least 6 characters"

    # Check for number and symbol in password
    has_num = False
    has_symbol = False

    for char in password:
        if char.isdigit():
            has_num = True
        elif not char.isalpha() and not char.isdigit():
            has_symbol = True

    if not has_num:
        return "Password must contain at least one number"
    elif not has_symbol:
        return "Password must contain at least one symbol"
    return None