from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt  # For hashing password
db = SQLAlchemy()
bcrypt = Bcrypt()

class URL(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(200),nullable=False)
    url_name = db.Column(db.String(300), nullable=False)
    url_link=db.Column(db.String(300),nullable=False)
    
    def __init__(self, email,url_name, url_link):
        """Constructor"""
        self.email=email
        self.url_name=url_name
        self.url_link=url_link

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(200),nullable=False,unique=True)
    username = db.Column(db.String(30), nullable=False)
    pwhash = db.Column(db.String(300), nullable=False)  # Store password hash 
    
    def __init__(self, email,username, password):
        """Constructor"""
        self.email=email
        self.pwhash = bcrypt.generate_password_hash(password)  # hash submitted password
        self.username = username
 
    def verify_password(self, password_in):
        return bcrypt.check_password_hash(self.pwhash, password_in)
        
def load_db(db):
    db.drop_all()
    db.create_all()
    db.session.add_all([User('user1@gmail.com',"123" ,'xxxx'),
                        User('user2@gmail.com',"134", 'yyyy')])  

    db.session.add_all([URL('user1@gmail.com',"gaana" ,'https://gaana.com/'),
                        URL('user2@gmail.com',"youtube", 'https://www.youtube.com/')]) 
    db.session.commit()