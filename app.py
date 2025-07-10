from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import markdown

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def html(self):
        return markdown.markdown(self.content, extensions=['fenced_code'])

def init_db():
    db.create_all()

@app.route('/')
def index():
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('index.html', title='Home', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html', title='New Post', post=None)

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('post', post_id=post.id))
    return render_template('create.html', title='Edit Post', post=post)

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
