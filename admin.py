from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite for testing
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
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    update_date = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, default=0)

# Course form
class CourseForm(FlaskForm):
    name = StringField('Course Name', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    price = StringField('Price', validators=[InputRequired()])
    image_url = StringField('Image URL', validators=[InputRequired()])
    update_date = StringField('Update Date', validators=[InputRequired()])
    rating = StringField('Rating', validators=[InputRequired()])
    submit = SubmitField('Submit')

# Admin route to add, edit, or remove courses
@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.username != 'admin':  # Only allow admin users
        return redirect(url_for('home'))
    
    courses = Course.query.all()
    return render_template('admin.html', courses=courses)

@app.route("/course/new", methods=['GET', 'POST'])
@login_required
def add_course():
    if current_user.username != 'admin':  # Only allow admin to add courses
        return redirect(url_for('home'))

    form = CourseForm()
    if form.validate_on_submit():
        course = Course(
            name=form.name.data,
            description=form.description.data,
            price=float(form.price.data),
            image_url=form.image_url.data,
            update_date=form.update_date.data,
            rating=int(form.rating.data)
        )
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('admin'))
    
    return render_template("create_course.html", form=form)

@app.route("/course/delete/<int:course_id>")
@login_required
def delete_course(course_id):
    if current_user.username != 'admin':  # Only allow admin to delete courses
        return redirect(url_for('home'))

    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('admin'))

# User authentication routes
@app.route("/login", methods=['GET', 'POST'])
def login():
    # Logic for logging in users, including validation of username/password
    pass

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# Home page route
@app.route("/")
def home():
    courses = Course.query.all()
    return render_template("home.html", courses=courses)

# Loading user function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)
