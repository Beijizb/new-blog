import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import markdown

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'changeme')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'password')

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    tags = db.Column(db.String(200), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def html(self):
        return markdown.markdown(self.content, extensions=['fenced_code'])

def init_db():
    db.create_all()

def login_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.path))
        return func(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['logged_in'] = True
            next_page = request.args.get('next') or url_for('index')
            return redirect(next_page)
    return render_template('login.html', title='Login')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form.get('category')
        tags = request.form.get('tags')
        new_post = Post(title=title, content=content, category=category, tags=tags)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html', title='New Post', post=None)

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.category = request.form.get('category')
        post.tags = request.form.get('tags')
        db.session.commit()
        return redirect(url_for('post', post_id=post.id))
    return render_template('create.html', title='Edit Post', post=post)

@app.route('/sitemap.xml')
def sitemap():
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('sitemap.xml', posts=posts), 200, {'Content-Type': 'application/xml'}

@app.route('/rss.xml')
def rss():
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('rss.xml', posts=posts), 200, {'Content-Type': 'application/rss+xml'}

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
