from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from .models import Event, Comment
from .forms import EventForm, CommentForm
from . import db, app
import os
from werkzeug.utils import secure_filename
#additional import:
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


bp = Blueprint('event', __name__, url_prefix='/events')

@bp.route('/<id>')
def show(id):
    event = Event.query.filter_by(id=id).first()
    # create the comment form
    cform = CommentForm()    
    return render_template('events/show.html', event=event, form=cform)

@bp.route('/create', methods=['GET', 'POST'])
#@login_required
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
            # Assuming you have these fields in your EventForm and Event model
            more_info=form.more_info.data if hasattr(form, 'more_info') else None,
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


@bp.route('/<event>/comment', methods = ['GET', 'POST'])  
@login_required
def comment(event):  
    form = CommentForm()  
    #get the destination object associated to the page and the comment
    event_obj = Event.query.filter_by(id=event).first()  
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data,  
                        event=event_obj,
                        user=current_user) 
      #here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 

      #flashing a message which needs to be handled by the html
      #flash('Your comment has been added', 'success')  
      print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('event.show', id=event))
    