import os
import random

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///books.db")


# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
#@login_required
def index():

    name = { "all": "", "n": "", "top": "", "uatop": "", "clas": "", "ua": "", "uabio": "", "uanonfic": "", "nonfic": "", "bio": "", "hist": "", "fant": "", "tril": "", "scific": ""}
    if request.method == "POST":

        """all"""
        n = random.randint(1,4738)
        top = random.randint(1039,2538)
        uatop = random.randint(609,709)
        clas = random.randint(4039,4438)
        ua = random.randint(1,608)
        uabio = random.randint(710,838)
        uanonfic = random.randint(839,1038)
        nonfic = random.randint(2539,3038)
        bio = random.randint(3039,3438)
        hist = random.randint(3439,3638)
        fant = random.randint(3639,3838)
        tril = random.randint(3839,4038)
        scific = random.randint(4439,4738)

        selected = request.form.get("categories")
        name[selected] = "selected"

        if selected == 'my':
            delete = db.execute("DELETE FROM temp")
            my = db.execute("SELECT * FROM my WHERE userID == ?", session["user_id"])
            count = 0
            for row in my:
                count +=1
                db.execute("INSERT  INTO temp (title, author, image, link, AuthorLink, num) VALUES (?, ?, ?, ?, ?, ?)", row["title"], row["author"], row["image"], row["link"], row["AuthorLink"], count)
            mycount = db.execute("SELECT COUNT(id) FROM temp")
            if mycount[0]["COUNT(id)"] < 1:
                apollogy = 'Додайте книги у список "Прочитати"!'
                return render_template("index.html", apollogy=apollogy, name=name)
            myrand = random.randint(1, mycount[0]["COUNT(id)"])
            sel = db.execute("SELECT * FROM temp WHERE num == ?", myrand)
            return render_template("index.html", sel=sel, name=name)

        elif selected == 'top':
            top = db.execute("SELECT * FROM books WHERE id == ?", top)
            return render_template("index.html", top=top, name=name)
        elif selected == 'uatop':
            uatop = db.execute("SELECT * FROM books WHERE id == ?", uatop)
            return render_template("index.html", uatop=uatop, name=name)
        elif selected == 'clas':
            clas = db.execute("SELECT * FROM books WHERE id == ?", clas)
            return render_template("index.html", clas=clas, name=name)
        elif selected == 'ua':
            ua = db.execute("SELECT * FROM books WHERE id == ?", ua)
            return render_template("index.html", ua=ua, name=name)
        elif selected == 'uabio':
            uabio = db.execute("SELECT * FROM books WHERE id == ?", uabio)
            return render_template("index.html", uabio=uabio, name=name)
        elif selected == 'uanonfic':
            uanonfic = db.execute("SELECT * FROM books WHERE id == ?", uanonfic)
            return render_template("index.html", uanonfic=uanonfic, name=name)
        elif selected == 'nonfic':
            nonfic = db.execute("SELECT * FROM books WHERE id == ?", nonfic)
            return render_template("index.html", nonfic=nonfic, name=name)
        elif selected == 'bio':
            bio = db.execute("SELECT * FROM books WHERE id == ?", bio)
            return render_template("index.html", bio=bio, name=name)
        elif selected == 'hist':
            hist = db.execute("SELECT * FROM books WHERE id == ?", hist)
            return render_template("index.html", hist=hist, name=name)
        elif selected == 'fant':
            fant = db.execute("SELECT * FROM books WHERE id == ?", fant)
            return render_template("index.html", fant=fant, name=name)
        elif selected == 'tril':
            tril = db.execute("SELECT * FROM books WHERE id == ?", tril)
            return render_template("index.html", tril=tril, name=name)
        elif selected == 'scific':
            scific = db.execute("SELECT * FROM books WHERE id == ?", scific)
            return render_template("index.html", scific=scific, name=name)
        elif selected == 'all':
            all = db.execute("SELECT * FROM books WHERE id == ?", n)
            return render_template("index.html", all=all, name=name)

        return render_template("index.html", name=name)
    return render_template("index.html", name=name)


@app.route("/add_book", methods=["GET", "POST"])
@login_required
def add_book():

    name = { "MyList": "", "READ": ""}

    if request.method == "POST":

        addinlists = request.form.get("lists")

        title = request.form.get("title")
        author = request.form.get("author")
        other = request.form.get("other")

        name[addinlists] = "selected"

        if addinlists == "MyList":
            db.execute("INSERT INTO my (userID, title, author, coments, image_sm, image) VALUES(?, ?, ?, ?, ?, ?)", session["user_id"], title, author, other, "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/nophoto/book/111x148._SX50_.png", "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/nophoto/book/111x148._SX175_.png")

        if addinlists == "READ":
            db.execute("INSERT INTO read (userID, title, author, notes, image_sm, image) VALUES(?, ?, ?, ?, ?, ?)", session["user_id"], title, author, other, "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/nophoto/book/111x148._SX50_.png", "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/nophoto/book/111x148._SX175_.png")
        return render_template("add_book.html", name=name)
    else:
        return render_template("add_book.html", name=name)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("потрібно ввести ім'я", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("потрібно ввести пароль", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("невірне ім'я і/або пароль", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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

        if not username or db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username")):
            return apology("ви не вели ім'я або користувач з таким іменем вже існує", 403)

        if not password or password != confirmation:
            return apology("ви не ввели пароль або ввели невірний пароль", 403)
        hash = generate_password_hash(password, method="pbkdf2:sha256")
        table = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        return render_template("login.html")
    else:
        return render_template("register.html")


@app.route("/my_list")
@login_required
def my_list():
    my = db.execute("SELECT * FROM my WHERE userID == ?", session['user_id'])
    return render_template("my_list.html", my=my)


@app.route("/top")
@login_required
def top():
    table = db.execute("SELECT * FROM books WHERE id BETWEEN ? AND ? AND LENGTH(title) < ?", 1039, 2538, 40)
    return render_template("top.html", table=table)


@app.route("/uatop")
@login_required
def uatop():
    table = db.execute("SELECT * FROM books WHERE id BETWEEN ? AND ? AND LENGTH(title) < ?",  609, 709, 40)
    return render_template("uatop.html", table=table)


@app.route("/clas")
@login_required
def clas():
    table = db.execute("SELECT * FROM books WHERE id BETWEEN ? AND ? AND LENGTH(title) < ?", 4039, 4438, 40)
    return render_template("clas.html", table=table)


@app.route("/ua")
@login_required
def ua():
    table = db.execute("SELECT * FROM books WHERE id BETWEEN ? AND ? AND LENGTH(title) < ?", 1, 608, 40)
    return render_template("ua.html", table=table)


@app.route("/uabio")
@login_required
def uabio():
    table = db.execute("SELECT * FROM books WHERE id BETWEEN ? AND ? AND LENGTH(title) < ?", 710, 838, 40)
    return render_template("uabio.html", table=table)


@app.route("/uanonfic")
@login_required
def uanonfic():
    table = db.execute("SELECT * FROM books WHERE id BETWEEN ? AND ? AND LENGTH(title) < ?", 839, 1038, 40)
    return render_template("uanonfic.html", table=table)


@app.route("/nonfic")
@login_required
def nonfic():
    table = db.execute("SELECT * FROM books WHERE id BETWEEN ? AND ? AND LENGTH(title) < ?", 2539, 3038, 40)
    return render_template("nonfic.html", table=table)


@app.route("/bio")
@login_required
def bio():
    table = db.execute("SELECT * FROM books WHERE id BETWEEN ? AND ? AND LENGTH(title) < ?", 3039, 3438, 40)
    return render_template("bio.html", table=table)


@app.route("/hist")
@login_required
def hist():
    table = db.execute("SELECT * FROM books WHERE id BETWEEN ? AND ? AND LENGTH(title) < ?",  3439, 3638, 40)
    return render_template("hist.html", table=table)


@app.route("/fant")
@login_required
def fant():
    table = db.execute("SELECT * FROM books WHERE id BETWEEN ? AND ? AND LENGTH(title) < ?", 3639, 3838, 40)
    return render_template("fant.html", table=table)


@app.route("/tril")
@login_required
def tril():
    table = db.execute("SELECT * FROM books WHERE id BETWEEN ? AND ? AND LENGTH(title) < ?", 3839, 4038, 40)
    return render_template("tril.html", table=table)


@app.route("/scific")
@login_required
def scific():
    table = db.execute("SELECT * FROM books WHERE id BETWEEN ? AND ? AND LENGTH(title) < ?", 4439, 4738, 40)
    return render_template("scific.html", table=table)

@app.route("/add", methods=["POST"])
def add():

    id = request.form.get("id")
    addID = request.form.get("addID")
    inread = request.form.get("read")

    book = db.execute("SELECT * FROM books WHERE id == ?", id)
    read = db.execute("SELECT * FROM my WHERE orderID == ? AND userID == ?", addID, session['user_id'])
    InRead = db.execute("SELECT * FROM books WHERE id == ?", inread)

    if id:
        db.execute("INSERT INTO my (userID, title, author, coments, image_sm, image) VALUES(?, ?, ?, ?, ?, ?)", session['user_id'], book[0]["title"], book[0]["author"], "-", book[0]["image_sm"],  book[0]["image"])
        if 1039 <= int(id) and int(id) <= 2538:
            return redirect("/top")
        if 609 <= int(id) and int(id) <= 709:
            return redirect("/uatop")
        if 4039 <= int(id) and int(id) <= 4438:
            return redirect("/klas")
        if 1 <= int(id) and int(id) <= 608:
            return redirect("/ua")
        if  710 <= int(id) and int(id) <= 838:
            return redirect("/uabio")
        if  839 <= int(id) and int(id) <= 1038:
            return redirect("/uanonfic")
        if  2539 <= int(id) and int(id) <= 3038:
            return redirect("/nonfic")
        if 3039 <= int(id) and int(id) <= 3438:
            return redirect("/bio")
        if 3439 <= int(id) and int(id) <= 3638:
            return redirect("/hist")
        if 3639 <= int(id) and int(id) <= 3838:
            return redirect("/fant")
        if 3839 <= int(id) and int(id) <= 4038:
            return redirect("/tril")
        if 4439 <= int(id) and int(id) <= 4738:
            return redirect("/scific")

    elif inread:
        db.execute("INSERT INTO read (userID, title, author, notes, image_sm, image) VALUES(?, ?, ?, ?, ?, ?)", session['user_id'], InRead[0]["title"], InRead[0]["author"], "-", InRead[0]["image_sm"], InRead[0]["image"])
        if 1039 <= int(inread) and int(inread) <= 2538:
            return redirect("/top")
        if 609 <= int(inread) and int(inread) <= 709:
            return redirect("/uatop")
        if 4039 <= int(inread) and int(inread) <= 4438:
            return redirect("/klas")
        if 1 <= int(inread) and int(inread) <= 608:
            return redirect("/ua")
        if  710 <= int(inread) and int(inread) <= 838:
            return redirect("/uabio")
        if  839 <= int(inread) and int(inread) <= 1038:
            return redirect("/uanonfic")
        if  2539 <= int(inread) and int(inread) <= 3038:
            return redirect("/nonfic")
        if 3039 <= int(inread) and int(inread) <= 3438:
            return redirect("/bio")
        if 3439 <= int(inread) and int(inread) <= 3638:
            return redirect("/hist")
        if 3639 <= int(inread) and int(inread) <= 3838:
            return redirect("/fant")
        if 3839 <= int(inread) and int(inread) <= 4038:
            return redirect("/tril")
        if 4439 <= int(inread) and int(inread) <= 4738:
            return redirect("/scific")

    elif addID:
        db.execute("INSERT INTO read (userID, title, author, notes, image_sm, image) VALUES(?, ?, ?, ?, ?, ?)", session['user_id'], read[0]["title"], read[0]["author"], "-", read[0]["image_sm"], read[0]["image"])
        db.execute("DELETE FROM my WHERE orderID = ?", addID)
        return redirect("/my_list")

    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    delete = request.form.get("delete")
    dell = request.form.get("dell")
    if delete:
        db.execute("DELETE FROM my WHERE orderID = ?", delete)
        return redirect("/my_list")
    elif dell:
        db.execute("DELETE FROM read WHERE id = ?", dell)
        return redirect("/read")
    return redirect("/")


@app.route("/read")
@login_required
def read():
    table = db.execute("SELECT * FROM read WHERE userID == ?", session['user_id'])
    return render_template("read.html", table=table)









