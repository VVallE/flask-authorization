from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship("Post", backref="author")  # uselist=False потрібен для One-to-One


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))


@app.route("/")
def index():
    return "AAAA"


@app.route("/posts_by_user", methods=["GET"])
def get_posts_by_user():
    user_name = request.args.get("user")

    if not user_name:
        return "User parameter is missing"

    user = User.query.filter_by(name=user_name).first()

    if not user:
        return "User not found"

    posts = Post.query.filter_by(author=user).all()

    if not posts:
        return "User has no posts"

    posts_data = [post.text for post in posts]
    return posts_data


def fill_database():
    data = [
        {"name": "Marshall Mathers", "text": "One two three to the four 1pac 2pac 3pac 4",
         "text2": "I`m not Afraid to bomb Belgorod"},
        {"name": "John Smith", "text": "Lama lama red pajama"},
        {"name": "Freddy Mercury", "text": "No time for loosers!",
         "text2": "We need put putin @under pressure@"},
    ]
    for pair in data:
        user = User(name=pair["name"])
        db.session.add(user)
        post = Post(text=pair["text"], author=user)
        db.session.add(post)
        if pair["name"] != "John Smith":
            post2 = Post(text=pair["text2"], author=user)
            db.session.add(post2)
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # fill_database()
    app.run(debug=True)
