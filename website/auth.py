from flask import Blueprint,render_template,redirect,request,flash,url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .import db
from flask_login import login_user, login_required, logout_user,current_user

auth = Blueprint('auth',__name__)


@auth.route('/login',methods = ['GET','POST'])
def login():
	if request.method == 'POST':
		user = None
		username = request.form.get('username')
		password = request.form.get('password')
		email = request.form.get('email')
		user_by_Username = User.query.filter_by(username=username).first()
		user_by_email = User.query.filter_by(email_address=username).first()

		if user_by_Username:
			user = user_by_Username
		elif user_by_email:
			user = user_by_email

		if user:
			if check_password_hash(user.password,password):
				flash('Logged in succesfully!',category='success')
				login_user(user,remember = True)
				return redirect(url_for('views.profile'))
			else:
				flash('Incorrect password, try again.',category='error')
		else:
			flash("Email does not exist.",category='error')
		
	return render_template('login_page.html')

@auth.route('/SignUp',methods = ['GET','POST'])
def SignUp():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		re_password = request.form.get('re_password')
		email = request.form.get('email')
		user = User.query.filter_by(username=username).first()
		
		if user is None:
			user = User.query.filter_by(email_address=email).first()
			if user is None:
				if password == re_password:
					new_user = User(username = username,password=generate_password_hash(password,method='sha256'),email_address=email)
					db.session.add(new_user)
					db.session.commit()
					login_user(new_user,remember = True)
					return redirect(url_for('views.profile'))
				else:
					flash('your verification pass is incorect',category='error')
			else:
				flash('email address already exist',category='error')
		else:
			flash('username already exist',category='error')


				
	return render_template('sign_up.html')

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	# return redirect(url_for('auth.login'))
	flash('Logout Succesfully',category='success')
	return redirect(url_for('views.home'))

@auth.route('/password_loss')
def password_loss():
	return render_template('password_loss.html')

@auth.route('/fde')
def fde():
	return render_template('feature_doesnt_exist.html')
