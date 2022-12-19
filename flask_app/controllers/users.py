from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)
app.secret_key='fkdkda'
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/register',methods=['POST'])
def register():
    if not user.User.validate_user(request.form):
        return redirect('/')
    pw_pass=bcrypt.generate_password_hash(request.form['password'])
    print(pw_pass)
    data={
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':pw_pass,

    }
    user.User.save(data)
    
    return redirect('/')
@app.route('/login',methods=['POST'])
def login():
    user_in_db=user.User.user_email(request.form['email'])
    if not user_in_db:
        flash('Invalid Email/Password','login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password,request.form['password']):
        flash('Invalid Email/Password','login')
        return redirect('/')
    
    session['user_id']=user_in_db.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
