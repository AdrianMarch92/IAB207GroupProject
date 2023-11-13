from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, DateField, TimeField, DecimalField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired, Regexp
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG','JPG','png','jpg'}

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    contact_number = IntegerField("Contact Number", validators=[InputRequired("Enter a contact number")])
    address = StringField("Address", validators=[InputRequired("Enter an address")])
    #linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[
        InputRequired(),
        Regexp('(?=.*\d)(?=.*[A-Z])', message="Password must contain at least one capital letter and one number."),
        EqualTo('confirm', message="Passwords should match")
    ])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    start_date = DateField('Start Date', validators=[InputRequired()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[InputRequired()], format='%Y-%m-%d')
    start_time = TimeField('Start Time', validators=[InputRequired()])
    end_time = TimeField('End Time', validators=[InputRequired()])
    ga_price = DecimalField('General Admission Price', validators=[InputRequired()])
    ga_availability = IntegerField('General Admission Availability', validators=[InputRequired()])
    concession_price = DecimalField('Concession Price', validators=[InputRequired()])
    concession_availability = IntegerField('Concession Availability', validators=[InputRequired()])
    vip_price = DecimalField('VIP Price', validators=[InputRequired()])
    vip_availability = IntegerField('VIP Availability', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    image = FileField('Event Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])
    event_guidelines = TextAreaField('Event Guidelines')
    terms_conditions = TextAreaField('Terms and Conditions')
    post_event = SubmitField("Post Event")
    status = SelectField(
        'Status',
        choices=[('open', 'Open'), ('sold_out', 'Sold Out'), ('closed', 'Closed')],
        validators=[DataRequired()]
    )
    category = SelectField(
        'Category',
        choices=[('asian', 'Asian'), ('indian', 'Indian'), ('italian', 'Italian'), ('greek', 'Greek'), ('european', 'European'), ('american', 'American')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Update Event')


class CommentForm(FlaskForm):
    text = TextAreaField('Comment', [InputRequired()])
    submit = SubmitField('Post')