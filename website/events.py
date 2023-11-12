from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from .models import Event, Comment, Bookings
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def check_upload_file():
    # Check if the post request has the file part
    if 'image' not in request.files:
        flash('No file part')
        return None
    file = request.files['image']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return None

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return file_path
    else:
        flash('Invalid file type')
        return None
    
def save_image(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return file_path 
    return None


bp = Blueprint('event', __name__, url_prefix='/events')

@bp.route('/event/<int:id>')
def event_details(id):
    print(f"Event ID: {id}")
    event = Event.query.get_or_404(id)
    comment_form = CommentForm()
    return render_template('eventDetails.html', event=event, form=comment_form)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    print('Method type: ', request.method)
    form = EventForm()
    if form.validate_on_submit():
        db_file_path = check_upload_file()
        print(db_file_path)

        # Instantiate an Event object with all the form fields
        event = Event(
            name=form.name.data,
            location=form.location.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            ga_price=form.ga_price.data,
            ga_availability=form.ga_availability.data,
            concession_price=form.concession_price.data,
            concession_availability=form.concession_availability.data,
            vip_price=form.vip_price.data,
            vip_availability=form.vip_availability.data,
            description=form.description.data,
            image=db_file_path,
            status=form.status.data,
            category=form.category.data,
            user_id=current_user.id,
            event_guidelines=form.event_guidelines.data,
            terms_conditions=form.terms_conditions.data
        )


        # Add the object to the db session
        db.session.add(event)

        # Commit to the database
        db.session.commit()
        print('Successfully created new event', 'success')

        # Always end with redirect when form is valid
        return redirect(url_for('event.create'))

    else:
      print("Form not validated")
      for fieldName, errorMessages in form.errors.items():
          for err in errorMessages:
              print(f"Error in {fieldName}: {err}")

    return render_template('events/createEvent.html', form=form)


@bp.route('/post_comment/<int:event_id>', methods=['POST'])
@login_required
def post_comment(event_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            text=form.text.data,
            event_id=event_id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added', 'success')
    else:
        flash('Error in comment submission', 'error')
    return redirect(url_for('event.event_details', id=event_id))
    
@bp.route('/profile')
@login_required
def profile():
    # Fetch events created by the current user
    created_events = Event.query.filter_by(user_id=current_user.id).all()
    booked_events = Bookings.query.filter_by(user_id=current_user.id).all()
    # Fetch events booked by the current user
    # This assumes you have a Booking model that links users to events they've booked
    booked_events = Bookings.query.filter_by(user_id=current_user.id).all()

    return render_template('profile.html', created_events=created_events, booked_events=booked_events)

@bp.route('/update_event/<int:id>', methods=['GET', 'POST'])
@login_required
def update_event(id):
    event = Event.query.get_or_404(id)

    # Check if the current user is the creator of the event
    if event.user_id != current_user.id:
        flash('You do not have permission to edit this event.')
        return redirect(url_for('event.show', id=id))

    form = EventForm(obj=event)  # Pre-populate the form with the event's data

    if form.validate_on_submit():
        # Update event with new form data
        event.name = form.name.data
        event.location = form.location.data
        event.start_date = form.start_date.data
        event.end_date = form.end_date.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.ga_price = form.ga_price.data
        event.ga_availability = form.ga_availability.data
        event.concession_price = form.concession_price.data
        event.concession_availability = form.concession_availability.data
        event.vip_price = form.vip_price.data
        event.vip_availability = form.vip_availability.data
        event.description = form.description.data
        if form.image.data:  # Check if a new file has been uploaded
            new_image_filename = save_image(form.image.data)
            if new_image_filename:
                event.image = new_image_filename 
        event.category = form.category.data
        event.event_guidelines = form.event_guidelines.data
        event.terms_conditions = form.terms_conditions.data
        try:
            db.session.commit()
            print("Successful update")
            flash('Event updated successfully.')
            return redirect(url_for('main.index'))
        except Exception as e:
            print("Error updating event:", e)
            db.session.rollback()
            flash('An error occurred. Event update failed.')

    else:
        print(form.errors) 

    return render_template('events/updateEvent.html', form=form, event=event)

@bp.route('/book_event/<int:id>', methods=['POST'])
@login_required
def book_event(id):
    total_cost = 0
    event = Event.query.get_or_404(id)
    ga_quantity = request.form.get('ga_quantity', type=int, default=0)
    concession_quantity = request.form.get('concession_quantity', type=int, default=0)
    vip_quantity = request.form.get('vip_quantity', type=int, default=0)

    total_cost = ga_quantity * event.ga_price + concession_quantity * event.concession_price + vip_quantity * event.vip_price
    # Create a new booking record
    booking = Bookings(
        name=event.name,
        description=event.description,
        image=event.image,
        user_id=current_user.id,
        event_id=id,
        ga_quantity=ga_quantity, 
        concession_quantity=concession_quantity,
        vip_quantity=vip_quantity 
    )

    # Add and commit to the database
    try:
        db.session.add(booking)
        db.session.commit()
        print("success!")
        flash('Booking successful!')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Booking failed.')
        print(e)

    return redirect(url_for('event.event_details', id=id))
