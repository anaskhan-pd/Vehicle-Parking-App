from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        address = request.form.get('address')
        pin_code = request.form.get('pin_code')

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists", 'error')
            return redirect(url_for('auth.register'))

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create user
        new_user = User(
            email=email,
            name=name,
            password=hashed_password,
            address=address,
            pin_code=pin_code,
            role='user'
        )

        db.session.add(new_user)
        db.session.commit()
        flash('Successfully Registered! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_role'] = user.role
            flash('Successfully logged in', 'success')

            if user.role == 'admin':
                return redirect(url_for('views.dashboard'))
            else:
                return redirect(url_for('views.available_lots')) 

        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('views.home'))
