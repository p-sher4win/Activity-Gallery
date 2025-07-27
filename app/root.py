from flask import Blueprint, render_template, redirect, url_for, request, flash
from cloudinary.uploader import upload as cloud_upload
from .webforms import ActivityForm
from .models import Activity, User
from flask_login import login_required, current_user


root = Blueprint('root', __name__, template_folder='templates')

# Admin Dashboard
@root.route('/dashboard')
@login_required
def dashboard():
    user_count = User.objects.count()
    activity_count = Activity.objects.count()
    recent_activity = Activity.objects.order_by('-date_added').first()

    return render_template('admin/dashboard.html', user_count=user_count, activity_count=activity_count, recent_activity=recent_activity)

# Upload Activity
@root.route('/add_activity', methods=['GET', 'POST'])
@login_required
def add_activity():
    form = ActivityForm()
    
    if form.validate_on_submit():
        img_urls = []
        for img_file in request.files.getlist('images'):
            if img_file:
                result = cloud_upload(img_file, folder='Activity-Arena')
                img_url = result.get('secure_url')
                img_urls.append(img_url)
        
        activity = Activity(
            title = form.title.data,
            img_urls = img_urls
        )
        activity.save()
        print
        return redirect(url_for('root.list_activities'))

    return render_template('admin/add_activity.html', form=form)

# List existing activities
@root.route('/list_activities')
@login_required
def list_activities():
    page = int(request.args.get('page', 1))
    per_page = 6

    total_activities = Activity.objects.count()
    total_pages = (total_activities + per_page - 1) // per_page

    activities = Activity.objects.order_by('-date_added').skip((page - 1) * per_page).limit(per_page)

    return render_template('admin/list_activities.html', activities=activities, page=page, total_pages=total_pages)

# List existing users
@root.route('/list_users')
@login_required
def list_users():
    users = User.objects.order_by('-date_added')

    return render_template('admin/list_users.html', users=users)