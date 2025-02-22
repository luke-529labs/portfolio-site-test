from flask import Flask, render_template, abort
from datetime import datetime

app = Flask(__name__)

# Sample data (in a real app, you'd use a database)
projects_data = [
    {
        "id": 1,
        "title": "Project One",
        "description": "Description of project one.",
        "image": "/static/images/project1.jpg",
        "link": "https://example.com/project1"
    },
    {
        "id": 2,
        "title": "Project Two",
        "description": "Description of project two.",
        "image": "/static/images/project2.jpg",
        "link": "https://example.com/project2"
    },
    {
        "id": 3,
        "title": "Project Three",
        "description": "Description of project three.",
        "image": "/static/images/project3.jpg",
        "link": "https://example.com/project3"
    },
    # Add more projects if needed...
]

blog_posts_data = [
    {
        "id": 1,
        "title": "Blog Post One",
        "summary": "Summary of blog post one.",
        "content": "<p>Full content of blog post one.</p>",
        "published_date": "2023-01-01",
        "image": "/static/images/blog1.jpg"
    },
    {
        "id": 2,
        "title": "Blog Post Two",
        "summary": "Summary of blog post two.",
        "content": "<p>Full content of blog post two.</p>",
        "published_date": "2023-02-15",
        "image": "/static/images/blog2.jpg"
    },
    {
        "id": 3,
        "title": "Blog Post Three",
        "summary": "Summary of blog post three.",
        "content": "<p>Full content of blog post three.</p>",
        "published_date": "2023-03-10",
        "image": "/static/images/blog3.jpg"
    },
    # More blog posts can be added...
]

@app.context_processor
def inject_current_year():
    return {"current_year": datetime.now().year}

@app.route('/')
def index():
    # For home, pick 3 featured projects and the 3 most recent blog posts
    featured_projects = projects_data[:3]
    recent_posts = blog_posts_data[:3]
    return render_template('index.html', featured_projects=featured_projects, recent_posts=recent_posts)

@app.route('/projects')
def projects():
    # Show all projects (you might want to sort these by date in a real app)
    return render_template('projects.html', projects=projects_data)

@app.route('/blog')
def blog():
    # Show all blog posts
    return render_template('blog.html', posts=blog_posts_data)

@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    # Find the blog post with the matching id
    post = next((post for post in blog_posts_data if post["id"] == post_id), None)
    if post is None:
        abort(404)
    return render_template('blog_post.html', post=post)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

