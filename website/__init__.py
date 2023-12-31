#from package import Class
from flask import Flask, render_template 
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db=SQLAlchemy()
app=Flask(__name__)

#create a function that creates a web application
# a web server will run this web application
def create_app():
  
    app=Flask(__name__)  # this is the name of the module/package that is calling this app
    app.debug=True
    app.secret_key='624142'
    #set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///cuisine_connect_db.sqlite'

    # Configuration
    UPLOAD_FOLDER = 'website/static/uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    os.makedirs(os.path.join(os.getcwd(), UPLOAD_FOLDER), exist_ok=True)

    #initialise db with flask app
    db.init_app(app)

    bootstrap = Bootstrap4(app)
    
    #initialize the login manager
    login_manager = LoginManager()
    
    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    #from .models import User  # importing here to avoid circular references
    #@login_manager.user_loader
    #def load_user(user_id):
    #    return User.query.get(int(user_id))
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #importing views module here to avoid circular references
    # a common practice.
    from . import views
    app.register_blueprint(views.bp)

    from . import events
    app.register_blueprint(events.bp)

    from . import auth
    app.register_blueprint(auth.bp)
    
    
    @app.errorhandler(404) 
    # inbuilt function which takes error as parameter 
    def not_found(e): 
        return render_template("404.html")

    return app

