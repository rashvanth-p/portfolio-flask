from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail, Message
import datetime
import os

# ================================
# APP INIT
# ================================
app = Flask(__name__)
CORS(app)

# ================================
# DATABASE CONFIG
# ================================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ================================
# EMAIL CONFIG (GMAIL SMTP)
# ================================
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

# Read from Railway environment variables
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_USERNAME")

# ================================
# INIT EXTENSIONS
# ================================
db = SQLAlchemy(app)
mail = Mail(app)

# ================================
# DATABASE MODEL
# ================================
class Contact(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow
    )

# ================================
# HOME ROUTE
# ================================
@app.route("/")
def home():
    return "Portfolio Backend Running"

# ================================
# CONTACT FORM API
# ================================
@app.route("/contact", methods=["POST"])
def contact():

    try:

        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        if not name or not email or not message:
            return jsonify({"error": "All fields required"}), 400

        # Save message in database
        new_message = Contact(
            name=name,
            email=email,
            message=message
        )

        db.session.add(new_message)
        db.session.commit()

        # Send email notification
        msg = Message(
            subject="New Portfolio Contact Message",
            recipients=[app.config["MAIL_USERNAME"]]
        )

        msg.body = f"""
New message from your portfolio

Name: {name}
Email: {email}

Message:
{message}
"""

        try:
            mail.send(msg)
            print("Email sent successfully")
        except Exception as mail_error:
            print("Email failed:", mail_error)

        return jsonify({
            "success": True,
            "message": "Message sent successfully"
        })

    except Exception as e:

        print("SERVER ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500


# ================================
# GET ALL MESSAGES
# ================================
@app.route("/messages")
def get_messages():

    try:

        messages = Contact.query.order_by(Contact.created_at.desc()).all()

        result = []

        for m in messages:
            result.append({
                "id": m.id,
                "name": m.name,
                "email": m.email,
                "message": m.message,
                "date": m.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================================
# TEST EMAIL ROUTE
# ================================
@app.route("/test-mail")
def test_mail():

    try:

        msg = Message(
            subject="Flask Test Email",
            recipients=[app.config["MAIL_USERNAME"]]
        )

        msg.body = "This is a test email from your Flask portfolio backend."

        mail.send(msg)

        return "Test email sent successfully"

    except Exception as e:
        return str(e)


# ================================
# RUN SERVER (Railway Compatible)
# ================================
if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 5000))

    print(f"Server running on port {port}")

    app.run(host="0.0.0.0", port=port)