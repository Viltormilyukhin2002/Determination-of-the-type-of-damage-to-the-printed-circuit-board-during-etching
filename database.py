from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cad = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)
    res = db.Column(db.Text)
    probability = db.Column(db.Text)
