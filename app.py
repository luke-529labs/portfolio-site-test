from flask import Flask, render_template, abort, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime

app = Flask(__name__)

# Configure your SQLite database and secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'testpassword'  # Change this in production!

# Set admin credentials (change these to secure values)
app.config['ADMIN_USERNAME'] = 'admin'
app.config['ADMIN_PASSWORD'] = 'secret'

db = SQLAlchemy(app)

# Define your models
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=True)
    link = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Project {self.title}>'

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=True)
    published_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<BlogPost {self.title}>'

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

@app.context_processor
def inject_current_year():
    return {"current_year": datetime.now().year}

@app.route('/')
def index():
    featured_projects = Project.query.order_by(Project.created_at.desc()).limit(3).all()
    recent_posts = BlogPost.query.order_by(BlogPost.published_date.desc()).limit(3).all()
    return render_template('index.html', featured_projects=featured_projects, recent_posts=recent_posts)

@app.route('/projects')
def projects():
    all_projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('projects.html', projects=all_projects)

@app.route('/blog')
def blog():
    posts = BlogPost.query.order_by(BlogPost.published_date.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('blog_post.html', post=post)

@app.route('/about')
def about():
    return render_template('about.html')

# -----------------------------
# Authentication for Admin Panel
# -----------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD']:
            session['logged_in'] = True
            flash("You were successfully logged in", "success")
            next_url = request.args.get('next')
            return redirect(next_url or url_for('admin.index'))
        else:
            flash("Invalid credentials", "error")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("You have been logged out", "success")
    return redirect(url_for('login'))

# Custom ModelView that restricts access to logged-in admins
class MyModelView(ModelView):
    def is_accessible(self):
        return session.get('logged_in', False)

    def inaccessible_callback(self, name, **kwargs):
        flash("Please log in to access the admin panel", "error")
        return redirect(url_for('login', next=request.url))

# Initialize Flask-Admin with secured views
admin = Admin(app, name='529labs Admin', template_mode='bootstrap3')
admin.add_view(MyModelView(Project, db.session))
admin.add_view(MyModelView(BlogPost, db.session))

if __name__ == '__main__':
    app.run(debug=True)


