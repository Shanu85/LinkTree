from flask import Blueprint,render_template,redirect,request,session
user=Blueprint("user", __name__)
from models import URL,db
from flask_login import login_required,current_user

@login_required
@user.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('/User/AllUrl.html')
    return redirect('/Login')

@login_required
@user.route('/add',methods=['GET', 'POST'])
def add():
    if current_user.is_authenticated:
        if request.method=="POST":
            urlName=request.form['urlName']
            urlLink=request.form['urlLink']
            newurl=URL("fake12@gmail.com", urlName, urlLink)
            db.session.add(newurl)
            db.session.commit()
            return redirect('/user')
        return render_template('/User/addUrl.html')
    return redirect('/Login')

@login_required
@user.route('/edit',methods=['GET', 'POST'])
def edit():
    if current_user.is_authenticated:
        if request.method=="POST":
            urlName=request.form['urlName']
            urlLink=request.form['urlLink']
            
            return redirect('/user')
        return render_template('/User/editUrl.html')    
    return redirect('/Login')

@login_required
@user.route('/deleteURL')
def deleteURL():
    if current_user.is_authenticated:
        print("Deleted")
        return redirect('/user')
    return redirect('/Login')
