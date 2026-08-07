from flask import Blueprint, render_template,request,session,redirect,url_for 
from datetime import datetime
import mysql.connector


from db import get_connection

db= get_connection()
booking_bp = Blueprint("booking" , __name__)
@booking_bp.route("/booking")
def booking():
    
    if "user_id" not in session:
        return redirect(url_for("login.login"))
    
    cursor=db.cursor(dictionary=True)
    
    if request.method == "POST":
        customer_name = request.form["customer_name"]
    
        email = request.form["email"]
    
        mobile = request.form["mobile"]
    
        driving_license = request.form["driving_license"]

        car_id = request.form["car_id"]

        pickup_date = request.form["pickup_date"]

        return_date = request.form["return_date"]

        pickup_time = request.form["pickup_time"]

        gender = request.form["gender"]

        payment_method = request.form["payment_method"]

        address = request.form["address"]

        extra_services = request.form.getlist("extra_services")

        extra_services_string = ",".join(extra_services)

        terms = request.form.get("terms")

        if not terms :
            cursor.close()
            return "Please accept Terms and Conditions" 
    
        cursor.execute("SELECT * FROM cars WHERE id=%s AND available = TRUE",(car_id,))
    
        car=cursor.fetchone()
           
    
        if not car :
            cursor.close()
    
            return "Selected car is not available."


        pickup = datetime.strptime(
            pickup_date,
            "%Y-%m-%d")
    
        return_day = datetime.strptime(
            return_date,
            "%Y-%m-%d")
        
        days = (return_day - pickup).days
        
        if days<= 0 :
            cursor.close()
            return"Return date must be after pickup date."
        
        total_amount=(days*float(car["price_per_day"]))
    
        query = """INSERT INTO bookings(
            customer_name,
            email,
            mobile,
            driving_license,
            car_id,
            pickup_date,
            return_date,
            pickup_time,
            gender,
            extra_services,
            payment_method,
            address,
            terms_accepted,
            total_amount,
            )
            VALUES(%s,%s,%s,%s,%s,
                   %s,%s,%s,%s,%s,
                   %s,%s,%s,%s)
            """
    
        values = (
    
                customer_name,
    
                email,
    
                mobile,
    
                driving_license,
    
                car_id,
    
                pickup_date,
    
                return_date,
    
                pickup_time,
    
                gender,
    
                extra_services_string,
    
                payment_method,
    
                address,
    
                True,
    
                total_amount,    
            )
        cursor.execute(query,values)
    
        db.commit()
        booking_id = cursor.lastrowid
    
        cursor.close()
    
        return render_template("booking_success.html",booking_id=booking_id,car=car,total_amount=total_amount,customer_name=customer_name)
    cursor.execute("SELECT *  FROM cars WHERE available = TRUE")
    cars=cursor.fetchall()
    cursor.close()
    return render_template("bookings.html",cars=cars)