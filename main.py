from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:juice@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'hhblg87uyiug'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self,username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup','index','post_entry']
    if request.endpoint not in allowed_routes and 'username' not in session:
        redirect ('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect ('/blog')
        else:
            flash("User password incorrect or user does not exist", 'error')

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        username_error = ''
        password_error = ''
        notmatch_error = ''

        if len(username) < 3 or len(username) > 20 or ' ' in username:
            username_error = 'Not a valid username'
    
        if len(password) < 3 or len(password) > 20 or ' ' in password:
            password_error = 'Not a valid password'

        if  verify != password:
            notmatch_error = 'Passwords must match'

        if username_error or password_error or notmatch_error:
            return render_template('signup.html', username_error=username_error, password_error=password_error, 
            notmatch_error=notmatch_error)

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect ('/blog')
        else:
            flash("Username already exists", 'error')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

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
        blog_owner = User.query.filter_by(username=session['username']).first

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