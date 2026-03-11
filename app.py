from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail, Message
import datetime

# ================================
# APP INIT
# ================================
app = Flask(__name__)

# Enable CORS
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

app.config["MAIL_USERNAME"] = "rashvanthpp18@gmail.com"
app.config["MAIL_PASSWORD"] = "gpad jjtu ajgn syvq"

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
# HOME ROUTE (LOAD HTML)
# ================================
@app.route("/")
def home():
    return render_template("index.html")

# ================================
# CONTACT FORM API
# ================================
@app.route("/contact", methods=["POST"])
def contact():

    try:

        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        if not name or not email or not message:
            return jsonify({"error": "All fields are required"}), 400

        # Save to database
        new_message = Contact(
            name=name,
            email=email,
            message=message
        )

        db.session.add(new_message)
        db.session.commit()

        # Send email
        msg = Message(
            subject="New Portfolio Contact Message",
            sender=app.config["MAIL_USERNAME"],
            recipients=[app.config["MAIL_USERNAME"]]
        )

        msg.body = f"""
New message from your portfolio website

Name: {name}
Email: {email}

Message:
{message}
"""

        mail.send(msg)

        return jsonify({
            "success": True,
            "message": "Message sent successfully"
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({"error": str(e)}), 500


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
            sender=app.config["MAIL_USERNAME"],
            recipients=[app.config["MAIL_USERNAME"]]
        )

        msg.body = "This is a test email from your Flask portfolio backend."

        mail.send(msg)

        return "Test email sent successfully"

    except Exception as e:

        return str(e)


# ================================
# RUN SERVER
# ================================
if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    print("Server running at http://127.0.0.1:5000")

    app.run(debug=True)