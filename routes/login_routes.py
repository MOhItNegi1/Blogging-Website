from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from extension import db
from models.profile import Profile
login = Blueprint('login', __name__, url_prefix='/login')

@login.route('/', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        role = request.form.get('role', '').strip()
        if role == 'visitor':
            session['username'] = 'Visitor'
            session['role'] = 'visitor'
            session.pop('user_id', None)  # Remove user_id if present
            flash('Logged in as visitor!', 'success')
            return redirect(url_for('post.show_posts'))
        else:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            user = User.query.filter_by(username=username, password=password, role=role).first()
            if user:
                session['username'] = user.username
                session['role'] = user.role
                session['user_id'] = user.id  # <-- Add this line
                flash(f'Logged in successfully as {user.role}!', 'success')
                return redirect(url_for('post.show_posts'))
            else:
                flash('Invalid credentials or role', 'error')
                return redirect(url_for('login.login_view'))
    return render_template('login.html')

@login.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'success')
    return redirect(url_for('login.login_view'))

@login.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm = request.form.get('confirm', '').strip()
        role = 'publisher'  

        if not username or not password or not confirm:
            flash('All fields are required.', 'error')
            return redirect(url_for('login.signup'))

        if password != confirm:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('login.signup'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already taken.', 'error')
            return redirect(url_for('login.signup'))

        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        new_profile = Profile(user_id=new_user.id)

        flash(f'Account created as {role}! You can now log in.', 'success')
        return redirect(url_for('login.login_view'))

    return render_template('signup.html')


@login.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        username = session.get('username')
        old_password = request.form.get('old_password', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not old_password or not new_password or not confirm_password:
            flash('All fields are required.', 'error')
            return redirect(url_for('login.change_password'))

        if new_password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('login.change_password'))

        user = User.query.filter_by(username=username, password=old_password).first()
        if not user:
            flash('Invalid old password.', 'error')
            return redirect(url_for('login.change_password'))

        user.password = new_password
        db.session.commit()

        flash('Password changed successfully.', 'success')
        return redirect(url_for('post.show_posts'))

    return render_template('change_password.html')

@login.route('/forget_password', methods=['POST'])
def forget_password():
    username = request.form.get('username', '').strip()
    new_password = request.form.get('new_password', '').strip()
    confirm_password = request.form.get('confirm_password', '').strip()

    if not username or not new_password or not confirm_password:
        flash('All fields are required.', 'error')
        return redirect(url_for('login.forget_password'))

    if new_password != confirm_password:
        flash('Passwords do not match.', 'error')
        return redirect(url_for('login.forget_password'))

    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('login.forget_password'))

    user.password = new_password
    db.session.commit()

    flash('Password reset successfully.', 'success')
    return redirect(url_for('login.login_view'))

@login.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('user_id'):
        flash('You must be logged in to view your profile.', 'error')
        return redirect(url_for('login.login_view'))
    profile = Profile.query.filter_by(user_id=session['user_id']).first()
    if not profile:
        # Create a profile if it doesn't exist
        profile = Profile(user_id=session['user_id'])
        db.session.add(profile)
        db.session.commit()
    if request.method == 'POST':
        profile.name = request.form.get('name', '').strip()
        profile.age = request.form.get('age', '').strip() or None
        profile.email = request.form.get('email', '').strip()
        profile.phone_no = request.form.get('phone_no', '').strip()
        profile.bio = request.form.get('bio', '').strip()
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('login.profile'))
    user = profile.user
    posts = user.posts
    return render_template('profile.html', user=user, profile=profile, posts=posts)