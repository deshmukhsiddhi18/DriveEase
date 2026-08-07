from flask import Flask,render_template,request,url_for,session,redirect,Blueprint
import mysql.connector
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from db import get_connection
from about import about_bp
from cars import cars_bp
from login import login_bp
from register import register_bp
from contact import contact_bp
from admin import admin_bp
from book import book_bp
from booking import booking_bp
from add_car import add_car_bp




app = Flask(__name__)
app.secret_key = "driveease_secret_key"
db = get_connection()
app.register_blueprint(about_bp)
app.register_blueprint(cars_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(book_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(add_car_bp)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/edit_car/<int:car_id>", methods=["GET","POST"])
def edit_car(car_id):

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        car_name = request.form["car_name"]

        brand = request.form["car_name"]

        fuel_type = request.form["fuel_type"]

        seats = request.form["seats"]

        price_per_day = request.form["price_per_day"]

        image = request.form["image"]

        available = request.form["available"]


        query = """
        UPDATE cars

        SET
            car_name = %s,
            brand = %s,
            fuel_type = %s,
            seats = %s,
            price_per_day = %s,
            image = %s,
            available = %s

        WHERE id = %s
        """


        values = (
            car_name,
            brand,
            fuel_type,
            seats,
            price_per_day,
            image,
            available,
            car_id
        )


        cursor.execute(query, values)

        db.commit()

        cursor.close()


        return redirect("/admin")


    cursor.execute(
        "SELECT * FROM cars WHERE id = %s",
        (car_id,)
    )


    car = cursor.fetchone()

    cursor.close()


    if not car:

        return "Car not found", 404


    return render_template(
        "edit_car.html",
        car=car
    )


@app.route("/delete_car/<int:car_id>")
def delete_car(car_id):
    cursor = db.cursor()

    cursor.execute("DELETE FROM cars WHERE id = %s", (car_id,))


    db.commit()

    cursor.close()


    return redirect("/admin")

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")

    cursor = db.cursor(dictionary=True)

    # Get logged-in customer
    cursor.execute(
        "SELECT * FROM users WHERE id = %s",
        (session["user_id"],)
    )

    user = cursor.fetchone()

    if not user:
        cursor.close()
        return "User not found"

    # Get customer's bookings
    cursor.execute(
        """
        SELECT
            bookings.*,
            cars.car_name,
            cars.brand
        FROM bookings
        JOIN cars
        ON bookings.car_id = cars.id
        WHERE bookings.email = %s
        ORDER BY bookings.id DESC
        """,
        (user["email"],)
    )

    bookings = cursor.fetchall()

    cursor.close()

    return render_template(
        "profile.html",
        user=user,
        bookings=bookings
    )


@app.route("/logout")
def logout():

    session.clear()

    return render_template("logout.html")


if __name__ == "__main__":
    app.run(debug=True)