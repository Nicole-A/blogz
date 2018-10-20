from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:juice@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner_id = owner


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='id')

    def __init__(self,username, password):
        self.username = username
        self.password = password
 


@app.route('/blog', methods=['POST', 'GET'])
def index():

    blog_title = request.args.get('blog_title')
    blog_id = request.args.get('id')

    if not blog_id:
        blogs = Blog.query.all()
        return render_template('blog.html',title="Build a Blog", blogs=blogs)
    else:
        blogs = Blog.query.get(blog_id)
        return render_template('display.html', title= "Blog Post",blogs=blogs)
    


@app.route('/newpost', methods=['POST', 'GET'])
def post_entry():

    if request.method == 'POST': 
        title_error = ''
        entry_error = ''
        blog_title = request.form['blog_title']
        blog_entry = request.form['body']
        blog_owner = ''

        if not blog_title:
            title_error = 'Enter a title'
            
        if not blog_entry:
            entry_error = 'Entry cannot be blank'

        if title_error or entry_error:
            return render_template('new_post.html',title="New Entry", blog_entry=blog_entry, title_error=title_error, entry_error=entry_error)
        else:     
            new_blog = Blog(blog_title, blog_entry, blog_owner)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog?id='+str(new_blog.id))
        
    return render_template('new_post.html',title="New Entry")


if __name__ == '__main__':
    app.run()