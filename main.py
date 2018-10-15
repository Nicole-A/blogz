from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:waterandice@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body =body

        
@app.route('/blog', methods=['POST', 'GET'])
def index():

    blog_title = request.args.get('blog_title')
    blogs = Blog.query.all()

    return render_template('blog.html',title="Build a Blog", blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def post_entry():
    if request.method == 'POST': 
        blog_title = request.form['blog_title']
        blog_entry = request.form['body']  
        new_blog = Blog(blog_title,blog_entry)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/blog')
    
    return render_template('new_post.html',title="New Entry")


if __name__ == '__main__':
    app.run()