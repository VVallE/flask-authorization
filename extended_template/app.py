from flask import Flask, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"  # database configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # binding DB and Flask App


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Создаем таблицу в контексте приложения
    app.run(debug=True)
