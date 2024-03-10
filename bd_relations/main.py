from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///documents.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), nullable=False)
    document = db.relationship("Document", backref="user", uselist=False)


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_name = db.Column(db.String(30), nullable=False)
    document_number = db.Column(db.String(30), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


@app.route("/create")
def index():
    user = User(full_name="Moo Tonom")
    doc = Document(document_name="driver license",
                   document_number="ABCDEFG123112",
                   user=user)

    db.session.add(user)
    db.session.add(doc)
    db.session.commit()

    return "User and Document created successfully!"


@app.route("/user/<int:user_id>/document")
def get_document(user_id):
    user = User.query.get_or_404(user_id)
    document = user.document
    if document:
        return f"{document.id}, {document.document_name}, {document.document_number}"
    else:
        return "User has no document"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
