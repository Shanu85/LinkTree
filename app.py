from flask import Flask,render_template,url_for,session,redirect,request,flash
from models import db,User,bcrypt,load_db
from user import user
from flask_login import LoginManager, login_user,login_required,current_user,logout_user

app=Flask(__name__)
bcrypt.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///allUser.db'
app.config['SECRET_KEY']="L7=f2[>4RT'D0$rA||*{WrAcIl7Bde"
db.init_app(app)
app.register_blueprint(user,url_prefix="/user")

login_manager=LoginManager()
login_manager.init_app(app)

with app.test_request_context():
    load_db(db)

@login_manager.user_loader
def load_user(id):
        return User.query.get(int(id))

@app.route('/')
def index():
    return render_template('index.html')

@login_required
@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect('/')
    else:
        return redirect('/Login')

@app.route('/SignUp',methods=['GET', 'POST'])
def SignUp():
    if not current_user.is_authenticated:
        if request.method == 'POST':
            username=request.form['UserName']
            email=request.form['Email']
            password=request.form['Password']
            
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email addess already exists.')
                return redirect('/SignUp')

            user=User(email, username, password)
            
            db.session.add(user)
            db.session.commit()
            return render_template('login.html')

        return render_template('register.html')
    else:
        return redirect('/user')

@app.route('/Login',methods=['GET', 'POST'])
def Login():
    if not current_user.is_authenticated:
        if request.method== 'POST':
            email=request.form['email']
            password=request.form['password']

            user = User.query.filter_by(email=email).first()

            if user!=None:
                if user.verify_password(password):
                    login_user(user)
                    return redirect('/user')
            
            flash('Please check your login details and try again!')
            return redirect('/Login')

        return render_template('login.html')
    else:
        return redirect('/user')

if __name__=="__main__":
    app.run(debug=True)
