from flask import Blueprint, render_template, flash, redirect, url_for, request
from .models import Activity
from mongoengine.errors import DoesNotExist

main = Blueprint('main', __name__, template_folder='templates')

# Home
@main.route('/')
def home():
    all_activities = Activity.objects.order_by('-date_added')
    activities = all_activities[:3]

    return render_template('public/home.html', activities=activities)

# Display all Activities
@main.route('/activities')
def activities():
    page = int(request.args.get('page', 1))
    per_page = 6

    total_activities = Activity.objects.count()
    total_pages = (total_activities + per_page - 1) // per_page

    activities = Activity.objects.order_by('-date_added').skip((page - 1) * per_page).limit(per_page)

    return render_template('public/activities.html', activities=activities, page=page, total_pages=total_pages)

# Each Activity
@main.route('/activity/<string:id>')
def get_activity(id):
    try:
        activity = Activity.objects.get(id=id)
    except DoesNotExist:
        flash("Activity not found!", category='error')
        return redirect(url_for('main.activities'))
    
    return render_template('public/activity.html', activity=activity)