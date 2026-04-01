from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "secret123"

# ===== DATABASE =====
def get_db():
    import os

DB_PATH = os.path.join(os.getcwd(), "amc.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS amc (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        location TEXT,
        contact_person TEXT,
        contact_no TEXT,
        email TEXT,
        po_no TEXT,
        po_date TEXT,
        system TEXT,
        visit_type TEXT,
        start TEXT,
        end TEXT,
        last_visit TEXT,
        engineer TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

# ===== LOGIN =====
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["user"] = "admin"
            return redirect("/dashboard")
    return render_template("login.html")

# ===== DASHBOARD =====
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    conn = get_db()
    data = conn.execute("SELECT * FROM amc").fetchall()
    conn.close()

    result = []
    for row in data:
        nv = datetime.strptime(row["last_visit"], "%Y-%m-%d") + timedelta(days=30)
        result.append((row, nv.strftime("%Y-%m-%d")))

    return render_template("dashboard.html", data=result)

# ===== ADD =====
@app.route("/add", methods=["POST"])
def add():
    conn = get_db()
    f = request.form

    conn.execute('''INSERT INTO amc 
    (name,location,contact_person,contact_no,email,po_no,po_date,system,visit_type,start,end,last_visit,engineer)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
    (f["name"], f["location"], f["cp"], f["cno"], f["email"],
     f["po_no"], f["po_date"], f["system"], f["visit"],
     f["start"], f["end"], f["last"], f["eng"]))

    conn.commit()
    conn.close()
    return redirect("/dashboard")

# ===== DELETE =====
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM amc WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/dashboard")

# ===== LOGOUT =====
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
