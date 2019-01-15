from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

cart = db.Table('cart',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(24), nullable=False)
	email = db.Column(db.String(80), nullable=False)
	pw_hash = db.Column(db.String(128), nullable=False)
	cart = db.relationship('Item', secondary=cart, lazy='subquery', backref=db.backref('users', lazy=True))
	
	def __init__(self, username, email, pw_hash):
		self.username = username
		self.email = email
		self.pw_hash = pw_hash

	def __repr__(self):
		return '<User {}>'.format(self.username)


class Address(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	street = db.Column(db.String(50), nullable=False)
	city = db.Column(db.String(50), nullable=False)
	state = db.Column(db.String(50), nullable=False)
	zip_code = db.Column(db.String(50), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, street, city, state, zip_code):
		self.street = street
		self.city = city
		self.state = state
		self.zip_code = zip_code

class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	in_stock = db.Column(db.Boolean, nullable=False)

	def __init__(self, name, in_stock):
		self.name = name
		self.in_stock = in_stock

