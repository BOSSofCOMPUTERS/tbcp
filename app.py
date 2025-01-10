from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Flask app and database setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models for the database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)

# Flask-WTForms for course creation
class CourseForm(FlaskForm):
    name = StringField('Course Name', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    category = StringField('Category', validators=[InputRequired()])
    submit = SubmitField('Create Course')

# Routes
@app.route("/")
def home():
    courses = Course.query.all()
    return render_template("home.html", courses=courses)

@app.route("/course/new", methods=['GET', 'POST'])
@login_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(name=form.name.data, description=form.description.data, category=form.category.data)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("create_course.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(../templates/index.html)
        else:
            return "Invalid username or password"
    return render_template("login.html")

from werkzeug.security import generate_password_hash, check_password_hash

# რეგისტრაციისას
hashed_password = generate_password_hash(password, method='sha256')

# შედარებისას
if check_password_hash(user.password, entered_password):
    login_user(user)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# Admin route (for admin to view all courses)
@app.route("/admin")
@login_required
def admin():
    if current_user.username != 'admin':  # Only allow admin users
        return redirect(url_for('home'))
    courses = Course.query.all()
    return render_template("admin.html", courses=courses)

# Load user function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)
