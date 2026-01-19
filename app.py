from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

# ================= APP CONFIG =================
app = Flask(__name__)   # templates/ and static/ folders are default


# ================= DATABASE CONNECTION =================
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ================= INITIALIZE DATABASE =================
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Table for table bookings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            booking_date TEXT,
            booking_time TEXT,
            guests INTEGER
        )
    """)

    # Table for contact messages
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    """)

    # Table for gift cards
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS giftcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient_name TEXT,
            recipient_email TEXT,
            amount INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ================= ROUTES =================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/menu")
def menu():
    return render_template("Menu.html")


@app.route("/contact")
def contact():
    return render_template("Contact us.html")


@app.route("/book-table")
def book_table():
    return render_template("Book_table.html")


@app.route("/giftcard")
def giftcard():
    return render_template("Giftcard.html")


@app.route("/private-hire")
def private_hire():
    return render_template("private_Hire.html")


@app.route("/thankyou")
def thankyou():
    return render_template("Thankyou.html")




# ================= FORM HANDLERS =================

# ---- Book Table ----
@app.route("/book", methods=["POST"])
def book():
    data = request.form
    conn = get_db()
    conn.execute("""
        INSERT INTO bookings (name, email, phone, booking_date, booking_time, guests)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["email"],
        data["phone"],
        data["booking_date"],
        data["booking_time"],
        data["guests"]
    ))
    conn.commit()
    conn.close()
    return redirect(url_for("thankyou"))


# ---- Contact Us ----
@app.route("/send-message", methods=["POST"])
def send_message():
    data = request.form
    conn = get_db()
    conn.execute("""
        INSERT INTO contacts (name, email, message)
        VALUES (?, ?, ?)
    """, (
        data["name"],
        data["email"],
        data["message"]
    ))
    conn.commit()
    conn.close()
    return redirect(url_for("thankyou"))


# ---- Buy Gift Card ----
@app.route("/buy-giftcard", methods=["POST"])
def buy_giftcard():
    data = request.form
    conn = get_db()
    conn.execute("""
        INSERT INTO giftcards (recipient_name, recipient_email, amount)
        VALUES (?, ?, ?)
    """, (
        data["recipient_name"],
        data["recipient_email"],
        data["amount"]
    ))
    conn.commit()
    conn.close()
    return redirect(url_for("thankyou"))


# ================= RUN APPLICATION =================
if __name__ == "__main__":
    init_db()              # create tables automatically
    app.run(debug=True)
