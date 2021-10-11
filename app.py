from os import name
from flask import Flask, render_template, request, redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:hamza1234@localhost:3306/fee"
app.config['SECRET_KEY'] = "tHIS iS MY first program"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Fee(db.Model):
    __tablename__ ="fee"
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    fee = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)



class Login(db.Model):
    __tablename__:"login"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.String(200), nullable=False)




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        username = request.form.get("username")
        password = request.form.get("password")
      
        user = Login.query.filter_by(username=username , password=password).first()
    
        if user:
            session["name"] = user.username
            return redirect("/")

    return render_template("login.html")   
    

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        
        roll_number = request.form.get("roll_number")
        name = request.form.get("name")
        fee = request.form.get("fee")

        user = Fee(roll_number=roll_number,name=name,fee=fee)
        db.session.add(user)
        db.session.commit()
        return redirect("/entry")       

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if session.get("name"):
       return render_template('base.html')
    else:
        return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")
        age = request.form.get("age")

        user = Login(username=username,password=password,name=name,age=age)
        db.session.add(user)
        db.session.commit()
        return redirect("/")        
    return render_template("register.html")




@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session['name'] = []
    return redirect('/')



@app.route('/show')
def products():
    if session.get("name"):
        allfee = Fee.query.all()
        return render_template('show.html', allfee=allfee)
    else:
        return render_template("login.html")

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method=='POST':
        roll_number = request.form['roll_number']
        name = request.form['name']
        feestatus = request.form['fee']
        fee = Fee.query.filter_by(id=id).first()
        fee.name=name
        fee.roll_number=roll_number
        fee.fee=feestatus   
        db.session.add(fee)
        db.session.commit()
        return redirect("/show")

    fee = Fee.query.filter_by(id=id).first()
    return render_template('update.html', fee=fee)

@app.route('/entry')
def entry():
    if session.get("name"):

        return render_template("insert.html")
    else:
        return render_template("login.html")

@app.route('/delete/<int:id>')
def delete(id):
    fee = Fee.query.filter_by(id=id).first()
    db.session.delete(fee)
    db.session.commit()
    return redirect("/show")

if __name__ == "__main__":
    app.run(debug=True, port=8000)