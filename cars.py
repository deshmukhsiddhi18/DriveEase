from flask import Blueprint, render_template

from db import get_connection

cars_bp = Blueprint("cars",__name__)
@cars_bp.route("/cars")
def cars():
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM cars WHERE available = TRUE")
    
    cars = cursor.fetchall()
    
    cursor.close()
    
    return render_template("cars.html", cars=cars)
