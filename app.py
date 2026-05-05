from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    conn = sqlite3.connect("database.db")
    return conn

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        db.close()

        if user:
            session["user"] = username
            return redirect("/")
        else:
            return "Login Failed. <a href='/login'>Try again</a>"

    return render_template("login.html")

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            db.commit()
        except:
            return "Registration Failed"
        finally:
            db.close()

        return redirect("/login")

    return render_template("register.html")

# Home
@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")

    db = get_db()
    data = db.execute("SELECT * FROM records").fetchall()
    db.close()
    return render_template("index.html", data=data)

# Add data
@app.route("/add", methods=["GET", "POST"])
def add():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        amount = request.form["amount"]
        date = request.form["date"]

        db = get_db()
        db.execute(
            "INSERT INTO records (name, amount, date) VALUES (?, ?, ?)",
            (name, amount, date)
        )
        db.commit()
        db.close()

        return redirect("/")

    return render_template("add.html")

# Logout
@app.route("/logout")

@app.route("/delete/<int:id>")
def delete(id):
    if "user" not in session:
        return redirect("/login")

    db = get_db()
    db.execute("DELETE FROM records WHERE id=?", (id,))
    db.commit()
    db.close()
    return redirect("/")
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')