from flask import Blueprint, render_template, redirect, url_for, flash
from .webforms import UserForm, LoginForm
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

# Define Blueprint
auth = Blueprint('auth', __name__, template_folder='templates')

# Login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # On Form submit
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if user:
            # Check password hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash(f"Welcome {user.username}", category='success')
                return redirect(url_for('root.dashboard'))
            else:
                flash("Wrong Password! - Try Again", category='error')
        else:
            flash("Invalid Username!", category='error')

    return render_template('public/login.html', form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged Out!", category='error')
    return redirect(url_for('main.home'))

################# Manage Users #################
# Add New User
@auth.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    name = None
    form = UserForm()

    if current_user.username == 'admin':
        if form.validate_on_submit():
            user = User.objects(username=form.username.data).first()
            if user:
                print("User Exists")

            if user is None:

                hashed_pswd = generate_password_hash(form.password_hash.data)
                
                user = User(
                    name = form.name.data,
                    username = form.username.data,
                    password_hash = hashed_pswd
                )
                user.save()
            
            form.name.data = ''
            form.username.data = ''
            
            flash("User Registered!", category='success')
            return redirect(url_for('root.dashboard'))

        all_users = User.objects.order_by('-date_created')

        return render_template('admin/add_user.html', form=form, name=name, all_users=all_users)
    else:
        flash("Sorry! only Admin user Authorized...", category='warning')
        return redirect(url_for('root.dashboard'))