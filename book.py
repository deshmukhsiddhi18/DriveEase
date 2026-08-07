from flask import Blueprint, render_template,request,session,redirect,url_for 

from db import get_connection
db = get_connection()


book_bp = Blueprint("book" , __name__)
@book_bp.route("/book")
def book():
    
    
    cursor=db.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM  cars WHERE available = True")

    
    cars = cursor.fetchall()
    cursor.close()
    return render_template("bookings.html",cars=cars)
    