from flask_login import UserMixin

from app import db, login


@login.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    # email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Preference(db.Model, UserMixin):
    entry = db.Column(db.Integer,primary_key=True)
    searchCount = db.Column(db.Integer, nullable=False)
    id = db.Column(db.Integer, nullable=False)
    topic = db.Column(db.String(200))
    duration = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.Integer)
    freePaid = db.Column(db.Integer, nullable=False)


class Course(db.Model):
    courseId = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.Text, nullable=False)
    link = db.Column(db.Text, nullable=False)
    categories = db.Column(db.Text, nullable=False)
    descriptionShort = db.Column(db.Text, nullable=False)
    descriptionLong = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    freeOption = db.Column(db.Integer, nullable=False)
    ratingNorm = db.Column(db.Float, nullable=False)
    paidOption = db.Column(db.Text, nullable=False)
    language = db.Column(db.Text, nullable=False)
    subtitle = db.Column(db.Text, nullable=False)
    platform = db.Column(db.Integer, nullable=False)
    provider = db.Column(db.Text, nullable=False)
    imageLink = db.Column(db.Text, nullable=False)


class Favourites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    courseId = db.Column(db.Integer, primary_key=True, nullable=False)

class Recommendations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    searchCount = db.Column(db.Integer, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    courseId = db.Column(db.Integer, primary_key=True, nullable=False)