from flask import Blueprint, render_template ,request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from email.message import EmailMessage
from db import get_connection

db = get_connection()


contact_bp = Blueprint("contact" , __name__)
@contact_bp.route("/contact",methods=["GET","POST"])
def contact():

    if request.method =="POST" :
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]

        sender_email= "deshmukhsiddhi042@gmail.com"
        app_password = "owrm jtid turo cglb"

        receiver_email = "deshmukhsiddhi042@gmail.com"

        msg = MIMEMultipart()

        msg["From"]= sender_email
        msg["To"]= receiver_email
        msg["Subject"]= f"DriveEase Contact - {subject}"
        body = f"""
                New Contact Message
                Name :{name}
                
                Email: {email}
                
                Subject : {subject}
 

                Meassage:
                {message}
                """
        msg.attach(MIMEText(body, "plain"))

        try:

            server = smtplib.SMTP("smtp.gmail.com", 587)

            server.starttls()

            server.login(sender_email, app_password)

            server.sendmail(
                sender_email,
                receiver_email,
                msg.as_string()
            )

            server.quit()

            return render_template(
                "contact.html",
                success="Message sent successfully!"
            )

        except Exception as e:

            return f"Error: {e}"
    return render_template("contact.html")
    