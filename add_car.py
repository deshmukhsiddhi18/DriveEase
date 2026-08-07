from flask import Blueprint, render_template,request,redirect
import mysql.connector 

from db import get_connection

db = get_connection()
add_car_bp = Blueprint("add_car" , __name__)
@add_car_bp.route("/add_car")
def add_car():
   
    if request.method == "POST":
    
            car_name = request.form["car_name"]
    
            brand = request.form["brand"]
    
            fuel_type = request.form["fuel_type"]
    
            seats = request.form["seats"]
    
            price_per_day = request.form["price_per_day"]
    
            image = request.form["image"]
    
            available = request.form["available"]
    
    
            cursor = db.cursor()
    
    
            query = """
            INSERT INTO cars
            (
                car_name,
                brand,
                fuel_type,
                seats,
                price_per_day,
                image,
                available
            )
            VALUES
            (
                %s, %s, %s, %s, %s, %s, %s
            )
            """
    
    
            values = (
                car_name,
                brand,
                fuel_type,
                seats,
                price_per_day,
                image,
                available
            )
    
    
            cursor.execute(query, values)
    
    
            db.commit()
    
    
            cursor.close()
    
    
            return redirect("/admin")
    return render_template("add_car.html")
    
    
