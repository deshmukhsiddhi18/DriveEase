from flask import Blueprint, render_template, request, session, redirect, url_for
import mysql.connector

from db import get_connection

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    db = get_connection()

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        user = cursor.fetchone()

        if not user:
            cursor.close()
            db.close()
            return render_template(
                "login.html",
                error="Email is not registered. Please register first."
            )

        if user["password"] != password:
            cursor.close()
            db.close()
            return render_template(
                "login.html",
                error="Incorrect password."
            )

        session["user_id"] = user["id"]

        cursor.close()
        db.close()

        return redirect(url_for("index"))

    return render_template("login.html")
