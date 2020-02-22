from flask import Flask, render_template, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bachat.sqlite3'

app.secret_key = "thisiseasy"
db = SQLAlchemy(app)

################################################MODELS###############################################

class flipkart(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable =True)
    link = db.Column(db.String(255), nullable =True)
    title = db.Column(db.String(100), nullable =True) 
    currrent_price = db.Column(db.String(14), nullable =True)
    #original_price = db.Column(db.String(15), nullabble =True)
    bachat = db.Column(db.String(50), nullable =True)
    date = db.Column(db.DateTime, nullable=False,default=datetime.now)

    def __repr__(self):
        return self.title+' from flipkart'

class snapdeal(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable =True) 
    link = db.Column(db.String(255), nullable =True)
    currrent_price = db.Column(db.String(14), nullable =True)
    discounted_price = db.Column(db.String(50), nullable =True)
    bachat = db.Column(db.String(50), nullable =True)
    date = db.Column(db.DateTime, nullable=False,default=datetime.now)

    def __repr__(self):
        return self.title+' from snapdeal'
    
class newegg(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable =True) 
    link = db.Column(db.String(255), nullable =True)
    currrent_price = db.Column(db.String(14), nullable =True)
    #discounted_price = db.Column(db.String(50), nullable =True)
    bachat = db.Column(db.String(50), nullable =True)
    date = db.Column(db.DateTime, nullable=False,default=datetime.now)

    def __repr__(self):
        return self.title+' from snapdeal'

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(50), nullable =True) 
    lastname = db.Column(db.String(50), nullable =True) 
    email = db.Column(db.String(50), nullable =True)
    password = db.Column(db.String(14), nullable =True)
    mobile= db.Column(db.Integer, nullable =True)
    pincode = db.Column(db.Integer, nullable =True)
    date = db.Column(db.DateTime, nullable=False,default=datetime.now) 



    def __repr__(self):
        return self.firstname
         
        
#####################################################################################################

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/display')
def display():
    df=pd.read_csv('shirts.csv')
    return render_template('display.html', data=df)

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        return validate_user(request)
    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        print('POST')
        firstname = request.form.get('firstname')
        print(firstname)
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        mobile = request.form.get('mobile')
        pincode= request.form.get('pincode')

        import time
        time.sleep(3)
        if firstname and lastname and email and password and mobile and pincode:
            user = User(firstname=firstname,lastname=lastname,email=email,
                            password=password,mobile=mobile,pincode=pincode)
            db.session.add(user)
            db.session.commit()
            print('success')
            return jsonify({'status':'success'})
        else:
            # show error to user
            return jsonify({'status':'invalid form data'})

    return render_template('register.html')
 
def validate_user(request):
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password:
        # check db for email and password
        flash("logged in successfully",'success')
        return redirect('/')
    else:
        flash("No details provided",'danger')
        return render_template('login.html')

@app.route('/search')
def search():
    return render_template('search.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)