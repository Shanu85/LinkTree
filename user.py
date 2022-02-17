from flask import Blueprint,render_template,redirect,request,session
user=Blueprint("user", __name__)
from models import URL,db
from flask_login import login_required,current_user
from models import User,URL,About

@login_required
@user.route('/')
def home():
    if current_user.is_authenticated:
        email=current_user.email
        user=User.query.filter_by(email=email).one()
        data=URL.query.filter_by(email=email).all()
        
        return render_template('/User/AllUrl.html',data=data,user=user)
    return redirect('/Login')

@login_required
@user.route('/info')
def info():
    if current_user.is_authenticated:
        email=current_user.email

        data1=About.query.filter_by(email=email).one()
        data2=len(URL.query.filter_by(email=email).all())
        data3=User.query.filter_by(email=email).one()
        
        return render_template('/User/updateInfo.html',about=data1.about,totalURL=data2,user=data3)
    return redirect('/Login')

@login_required
@user.route('/updateInfo',methods=['GET', 'POST'])
def updateInfo():
    if current_user.is_authenticated:
        if request.method=="POST":
            
            email=current_user.email

            name=request.form['username']
            password=request.form['password']
            about=request.form['about']

            newuser=User(email,name,password)

            User.query.filter_by(id=current_user.id).update({'email':email,'username':name,'pwhash':newuser.pwhash})
            About.query.filter_by(id=current_user.id).update({'email':email,'about':about})
            db.session.commit()

        return redirect('/user')

    else:
        return redirect('/')

@login_required
@user.route('/add',methods=['GET', 'POST'])
def add():
    if current_user.is_authenticated:
        email=current_user.email
        if request.method=="POST":
            urlName=request.form['urlName']
            urlLink=request.form['urlLink']
            newurl=URL(email,urlName,urlLink)
            db.session.add(newurl)
            db.session.commit()
            return redirect('/user')
        return render_template('/User/addUrl.html')
    return redirect('/Login')

@login_required
@user.route('/edit/<int:url_id>',methods=['GET', 'POST'])
def edit(url_id):
    if current_user.is_authenticated:
        email=current_user.email
        data=URL.query.filter_by(email=email,id=url_id).all()
        
        if request.method=="POST":
            urlName=request.form['urlName']
            urlLink=request.form['urlLink']
            
            URL.query.filter_by(id=url_id).update({'url_name':urlName,'url_link':urlLink})
            db.session.commit()

            return redirect('/user')
        return render_template('/User/editUrl.html',data=data)    
    return redirect('/Login')

@login_required
@user.route('/deleteURL/<int:url_id>')
def deleteURL(url_id):
    if current_user.is_authenticated:
        URL.query.filter_by(id=url_id).delete()
        db.session.commit()
        return redirect('/user')
    return redirect('/Login')

