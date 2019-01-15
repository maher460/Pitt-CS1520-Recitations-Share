from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
from models import db, User, Item
from werkzeug import check_password_hash, generate_password_hash

### Initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "my_super_secret_key_123434"
db.init_app(app)

@app.cli.command('initdb')
def initdb_command():
	"""Creates the database tables."""
	db.drop_all()
	db.create_all()
	print('Initialized the database.')

@app.cli.command('populate_dummy_data')
def populate_dummy_data_command():

	user1 = User("maher456", "maher456@gmail.com", generate_password_hash("45678"))
	db.session.add(user1)

	item1 = Item("A4 Paper", True)
	item2 = Item("Marker", True)
	item3 = Item("Stapler", True)

	db.session.add(item1)
	db.session.add(item2)
	db.session.add(item3)

	user1.cart.append(item2)
	user1.cart.append(item3)
	
	# commit
	db.session.commit()
	print('Populated DB with dummy data')

### Helper functions
def get_user_id(username):
	"""Convenience method to look up the id for a username."""
	rv = User.query.filter_by(username=username).first()
	return rv.id if rv else None

@app.before_request
def before_request():
	g.user = None
	if 'user_id' in session:
		g.user = User.query.filter_by(id=session['user_id']).first()



### Endpoint Controllers	

@app.route("/")
def hello():
	return render_template('home.html')

@app.route("/shop")
def shop():
	if not g.user:
		return redirect(url_for('login'))
	else:
		items = Item.query.all()
	return render_template('shop.html', items = items)

@app.route("/cart")
def cart():
	if not g.user:
		return redirect(url_for('login'))
	else:
		items = g.user.cart
	return render_template('cart.html', items = items)

@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Logs the user in."""
	if g.user:
		return redirect(url_for('shop'))
	error = None
	if request.method == 'POST':

		user = User.query.filter_by(username=request.form['username']).first()
		if user is None:
			error = 'Invalid username'
		elif not check_password_hash(user.pw_hash, request.form['password']):
			error = 'Invalid password'
		else:
			flash('You were logged in')
			session['user_id'] = user.id
			return redirect(url_for('shop'))
	return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
	"""Registers the user."""
	if g.user:
		return redirect(url_for('shop'))
	error = None
	if request.method == 'POST':
		if not request.form['username']:
			error = 'You have to enter a username'
		elif not request.form['email'] or \
				'@' not in request.form['email']:
			error = 'You have to enter a valid email address'
		elif not request.form['password']:
			error = 'You have to enter a password'
		elif request.form['password'] != request.form['password2']:
			error = 'The two passwords do not match'
		elif get_user_id(request.form['username']) is not None:
			error = 'The username is already taken'
		else:
			db.session.add(User(request.form['username'], request.form['email'], generate_password_hash(request.form['password'])))
			db.session.commit()
			flash('You were successfully registered and can login now')
			return redirect(url_for('login'))
	return render_template('register.html', error=error)


@app.route('/logout')
def logout():
	"""Logs the user out."""
	flash('You were logged out')
	session.pop('user_id', None)
	return redirect(url_for('login'))

	
