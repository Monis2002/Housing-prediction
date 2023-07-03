from flask import Flask,render_template,request,url_for,jsonify
import json
import pandas as pd
from forms import Take_data
from flask_sqlalchemy import SQLAlchemy
import os
import util

df=pd.read_csv("File_LPB.csv")
global __locations
with open("./artifacts/columns.json", "r") as f:
    __data_columns = json.load(f)['data_columns']
    __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

#img_folder=os.path.join("images")

app=Flask(__name__)
app._static_folder ='PBL(2nd )'

app.config["SECRET_KEY"]="452353245monismof32r4"
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///site.db'
#app.config["UPLOAD_FOLDER"]=img_folder

db=SQLAlchemy(app)

# Creating an table with Fields

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    budget=db.Column(db.Integer,nullable=False)
    BHK=db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"User('{self.budget}','{self.BHK}')"

#class Result_database(db.Model):
#    id=db.Column(db.Integer,primary_key=True)
#    location=db.Column(db.String(40),nullable=False)
#    bhk=db.Column(db.Integer,nullable=False)
#    price=db.Column(db.Float,nullable=False)

#    def __repr__(self):
#        return f"Result_database('{self.location}','{self.bhk}','{self.price}')"


# From server File
@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    response = jsonify({
        'estimated_price': util.get_estimated_price(location,total_sqft,bhk,bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

# End of server File

@app.before_first_request
def delete_tables():
     db.drop_all()

#@app.before_first_request
#def create_tables():
 #    db.create_all()


@app.route("/search",methods=["GET","POST"])
def home():
    if not os.path.exists("site.db"):
        db.create_all()
    form=Take_data()

    if request.method=="POST":
        if form.validate_on_submit():
            db.drop_all()
            db.create_all()
            user=User(BHK=form.BHK.data,budget=form.budget.data)
            db.session.add(user)
            db.session.commit()




    u = User.query.all()

    r,l=df.shape


    df_location=list(df.location)
    df_bhk=list(df.bhk)
    df_price=list(df.predict_price)
    df_sqft=list(df.total_sqft)

    price=[]

    #none_list=[None]
   # result=Result_database.query.all()
   # return render_template('Home.html',form=form,u=u,location=location,df=df,r=r)

   # pic=os.path.join(app.config["UPLOAD_FOLDER"],'house.jpeg')

    return render_template('home1.html',form=form,u=u,df=df,r=r,df_location=df_location,df_bhk=df_bhk,df_price=df_price,price=price,df_sqft=df_sqft,url_for=url_for)




if __name__=="__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(debug="False")

