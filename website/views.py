from flask import Blueprint, render_template, request, redirect,url_for, current_app, jsonify
from .models import Event, Comment, Bookings
from .forms import EventForm, CommentForm
from flask_login import login_required, current_user

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    events = Event.query.all()
    recommended_events = Event.query.order_by(Event.id.desc()).limit(4).all()
    all_events = Event.query.all() 
    return render_template('index.html', events=events, recommended_events=recommended_events, all_events=all_events)

@bp.route('/filter_events', methods=['POST'])
def filter_events():
    search_query = request.form.get('search', '')
    selected_categories = request.form.getlist('category')
    print(search_query)
    print(selected_categories)

    events = Event.query
    if selected_categories:
        events = events.filter(Event.category.in_(selected_categories))
    if search_query:
        events = events.filter(Event.name.ilike(f'%{search_query}%'))
    events = events.all()

    return render_template('index.html', events=events)
