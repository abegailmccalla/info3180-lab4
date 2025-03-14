import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.models import UserProfile
from app.forms import LoginForm
from app.forms import UploadForm
from werkzeug.security import check_password_hash
from flask import send_from_directory
from werkzeug.exceptions import BadRequest


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Abegail McCalla")

def get_uploaded_images():
     rootdir = os.getcwd()    
     file_list = []
 
     for subdir, dirs, files in os.walk(rootdir + r'\uploads'):
         for file in files:
             file_list.append(file)
     return file_list

@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

@app.route('/files')
@login_required
def files():
    images = get_uploaded_images()
    return render_template('files.html', images=images)

@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    # Instantiate your form class
    #form = LoginForm()
    form = UploadForm()
    # Validate file upload on submit
    if form.validate_on_submit():
        # Get file data and save to your uploads folder
        file = form.photo.data

         # Save the file securely to the uploads folder
        filename = secure_filename(file.filename)

        #app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('File Saved', 'success')
        return redirect(url_for('files')) # Update this to redirect the user to a route that displays all uploaded image files        
    return render_template('upload.html', form = form)

############# USING UPLOADS HTML (uploads.html) #######################
# @app.route('/view_uploads')
# def view_uploads():
#     """Display all uploaded images."""
#     uploads_folder = app.config['UPLOAD_FOLDER']
#     try:
#         image_files = os.listdir(uploads_folder)  # List all files in the uploads directory
#         image_files = [f for f in image_files if f.endswith(('jpg', 'png'))]  # Filter image files
#         return render_template('uploads.html', images=image_files)
#     except FileNotFoundError:
#         flash('Uploads folder not found!', 'danger')
#         return redirect(url_for('home'))

# @app.route('/uploaded_file/<filename>')
# def uploaded_file(filename):
#     """Serve uploaded files dynamically."""
#     return send_from_directory(os.path.join(os.getcwd(), 'uploads'), filename)
###########################################################################################


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    # change this to actually validate the entire form submission
    # and not just one field
    if form.validate_on_submit():
        # Get the username and password values from the form.
        username = form.username.data
        password = form.password.data

        # Using your model, query database for a user based on the username
        # and password submitted. Remember you need to compare the password hash.
        # You will need to import the appropriate function to do so.
        # Then store the result of that query to a `user` variable so it can be
        # passed to the login_user() method below.
        if db.session.execute(db.select(UserProfile).filter_by(username=username)).scalar():
            user = db.session.execute(db.select(UserProfile).filter_by(username=username)).scalar()
            ses_username = user.username
            ses_password = user.password
        else:
            flash('Username or Password is incorrect.', 'danger') 
            return redirect(url_for('login'))
        
        # Gets user id, load into session
        if user and check_password_hash(ses_password, password):
            flash('Logged in successfully.', 'success')
            login_user(user)
            # Remember to flash a message to the user
            return redirect(url_for("upload"))  # The user should be redirected to the upload form instead
        else:
            flash('Username or Password is incorrect.', 'danger') 
            return redirect(url_for('login'))
        
    return render_template("login.html", form=form)

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(UserProfile).filter_by(id=id)).scalar()

###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
