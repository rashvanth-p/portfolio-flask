from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)

# ==============================
# DATABASE CONFIG
# ==============================

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# ==============================
# EMAIL CONFIG (GMAIL SMTP)
# ==============================

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True

# CHANGE THESE
app.config["MAIL_USERNAME"] = "rashvanthpp18@gmail.com"
app.config["MAIL_PASSWORD"] = "rmjovfszaakuqfuq"

app.config["MAIL_DEFAULT_SENDER"] = "rashvanthpp18@gmail.com"


# ==============================
# INIT EXTENSIONS
# ==============================

db = SQLAlchemy(app)
mail = Mail(app)
CORS(app)


# ==============================
# DATABASE MODEL
# ==============================

class Contact(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), nullable=False)

    message = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# create database
with app.app_context():
    db.create_all()


# ==============================
# HOME ROUTE
# ==============================

@app.route("/")
def home():
    return render_template("index.html")


# ==============================
# CONTACT API
# ==============================

@app.route("/contact", methods=["POST"])
def contact():

    try:

        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        if not name or not email or not message:
            return jsonify({
                "error": "All fields are required"
            }), 400


        # SAVE TO DATABASE
        new_contact = Contact(
            name=name,
            email=email,
            message=message
        )

        db.session.add(new_contact)
        db.session.commit()


        # SEND EMAIL TO YOU
        msg = Message(
            subject="New Portfolio Contact Message",
            recipients=[app.config["MAIL_USERNAME"]]
        )

        msg.body = f"""
You received a new message from your portfolio website.

Name: {name}
Email: {email}

Message:
{message}

Time: {datetime.utcnow()}
"""

        mail.send(msg)


        return jsonify({
            "message": "Message sent successfully"
        }), 200


    except Exception as e:

        return jsonify({
            "error": "Server error",
            "details": str(e)
        }), 500


# ==============================
# VIEW MESSAGES API (OPTIONAL)
# ==============================

@app.route("/messages", methods=["GET"])
def get_messages():

    messages = Contact.query.order_by(Contact.created_at.desc()).all()

    result = []

    for msg in messages:

        result.append({
            "id": msg.id,
            "name": msg.name,
            "email": msg.email,
            "message": msg.message,
            "created_at": msg.created_at
        })

    return jsonify(result)


# ==============================
# RUN SERVER
# ==============================

if __name__ == "__main__":
    app.run(debug=True)