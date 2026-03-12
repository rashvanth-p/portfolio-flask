from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)

# DATABASE CONFIG
basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)


# DATABASE MODEL
class Contact(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), nullable=False)

    message = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# CONTACT API (SAVE ONLY)
@app.route("/contact", methods=["POST"])
def contact():

    try:

        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        if not name or not email or not message:
            return jsonify({"error": "All fields required"}), 400

        new_contact = Contact(
            name=name,
            email=email,
            message=message
        )

        db.session.add(new_contact)
        db.session.commit()

        return jsonify({"message": "Saved successfully"}), 200

    except Exception as e:

        return jsonify({
            "error": "Server error",
            "details": str(e)
        }), 500


# VIEW MESSAGES
@app.route("/messages")
def get_messages():

    messages = Contact.query.order_by(Contact.created_at.desc()).all()

    result = []

    for msg in messages:

        result.append({
            "name": msg.name,
            "email": msg.email,
            "message": msg.message,
            "created_at": msg.created_at
        })

    return jsonify(result)


# RUN SERVER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)