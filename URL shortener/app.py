import os
from flask import Flask , render_template , request , redirect 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random 
import string
app = Flask(__name__) 
base_dir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+ os.path.join(base_dir,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db = SQLAlchemy(app) 
Migrate(db,app)

@app.before_first_request
def create_table():
    db.create_all()


class url(db.Model):
    __tablename__= 'urls'
    id=db.Column(db.Integer,primary_key=True)
    user_url=db.Column(db.Text)
    short_url=db.Column(db.Text)
    def __init__(self, user_url, short_url):
        self.user_url = user_url
        self.short_url = short_url
    def __repr__(self): 
        return "Original_url ::: {}   and  short_url  ::: {}".format(self.user_url , self.short_url)

data ={}
@app.route("/")
def home_get():
    return render_template("index.html")

@app.route("/" , methods = ['POST'])
def home_post():
        himalayan = 5
        original_url = request.form.get("inp_1")
        short_url_1 = "".join(random.choices(string.ascii_letters+string.digits ,k = himalayan ))
        data[short_url_1] = original_url
        new_url = url(original_url , short_url_1)
        db.session.add(new_url)
        db.session.commit()
        return render_template("index.html" , k = short_url_1 )
    
@app.route("/history")
def fun_2():
    all_urls = url.query.all()
    return render_template("history.html" , data = data , all_urls = all_urls )

@app.route("/srivarshithdaladuli/<short>")
def fun_3(short):
    if(short) in data :
        return redirect(data[short])
    return "incorrect url"
    
if __name__ == "__main__":
    app.run(debug =True)
        


    
