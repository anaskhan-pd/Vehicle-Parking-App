from flask import Blueprint, render_template, request, flash, redirect,url_for, session
from .models import db,User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        address = request.form.get('address')
        pin_code = request.form.get('pin_code')

        existing_user = User.query.filter_by(email= email).first()
        if existing_user:
            flash("Email already exists", 'error')
            return redirect(url_for('auth.register'))
        
        new_user = User(
            email=email,
            name=name,
            password=generate_password_hash(password),
            address=address,
            pin_code=pin_code,
            role = 'user' 
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Succesfully Registered', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password', 'error')
            return redirect(url_for('auth.login'))
        
        session['user_id']= user.id
        session['user_role'] = user.role
        flash('Successfully logged in', 'success')

        if user.role == 'admin':
            return redirect(url_for('views.dashboard'))
        else:
            return redirect(url_for('views.home'))
    
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    flash('Logged out' , 'success')
    return redirect(url_for('views.home'))





