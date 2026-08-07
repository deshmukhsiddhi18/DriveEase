from flask import Blueprint, render_template,request,session,redirect 

from db import get_connection


register_bp = Blueprint("register" , __name__)
@register_bp.route("/register")
def register():
    db = get_connection()
    if request.method == "POST":    
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        cursor = db.cursor()

        query = """
        INSERT INTO users
        (firstname, lastname, email, phone, password)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            firstname,
            lastname,
            email,
            phone,
            password
        )
        
        cursor.execute(query, values)

        db.commit()

        cursor.close()

        return render_template("login.html")
    return render_template("register.html")