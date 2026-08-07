from flask import render_template,request,url_for,session,Blueprint,redirect
import mysql.connector

from db import get_connection
db = get_connection()

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin_login",methods=["GET","POST"])
def admin_login():
    
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username, password)
        )

        admin = cursor.fetchone()

        cursor.close()

        if admin:

            session["admin_id"] = admin["id"]

            return redirect(url_for("admin.admin"))

        else:

            return render_template(
                "admin_login.html",
                error="Invalid username or password."
            )
    return render_template("admin_login.html")



@admin_bp.route("/admin")
def admin():

    if "admin_id" not in session:
        return redirect(url_for("admin.admin_login"))

    cursor = db.cursor(dictionary=True)

     
    query = """
    SELECT 
        bookings.id,
        bookings.customer_name,
        bookings.email,
        bookings.mobile,
        bookings.driving_license,
        bookings.pickup_date,
        bookings.return_date,
        bookings.pickup_time,
        bookings.gender,
        bookings.extra_services,
        bookings.payment_method,
        bookings.address,
        bookings.total_amount,
        cars.car_name,
        cars.brand

    FROM bookings

    JOIN cars
    ON bookings.car_id = cars.id

    ORDER BY bookings.id DESC
    """

    cursor.execute(query)

    bookings = cursor.fetchall()


    # Count total cars

    cursor.execute(
        "SELECT COUNT(*) AS total_cars FROM cars"
    )

    total_cars = cursor.fetchone()["total_cars"]


    # Count total users

    cursor.execute(
        "SELECT COUNT(*) AS total_users FROM users"
    )

    total_users = cursor.fetchone()["total_users"]


    # Count total bookings

    cursor.execute(
        "SELECT COUNT(*) AS total_bookings FROM bookings"
    )

    total_bookings = cursor.fetchone()["total_bookings"]


    # Calculate total revenue

    cursor.execute(
        "SELECT COALESCE(SUM(total_amount), 0) AS total_revenue FROM bookings"
    )

    total_revenue = cursor.fetchone()["total_revenue"]

    cursor.execute("SELECT * FROM cars ORDER BY id DESC")

    all_cars = cursor.fetchall()


    cursor.close()


    return render_template(
        "admin.html",
        bookings=bookings,
        all_cars=all_cars,
        total_cars=total_cars,
        total_users=total_users,
        total_bookings=total_bookings,
        total_revenue=total_revenue
    )    

@admin_bp.route("/admin_logout")
def admin_logout():

    session.pop("admin_id", None)

    return redirect(url_for("admin.admin_login"))
