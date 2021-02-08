#from flask import Flask 
from flask import Flask, render_template, redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash


from random import *

#start-pg.sh

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///hzville"
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")


@app.route("/")
def index():
    result = db.session.execute("SELECT COUNT(*) FROM messages")
    count = result.fetchone()[0]
    result = db.session.execute("SELECT content FROM messages")
    messages = result.fetchall()
    return render_template("index.html", count=count, messages=messages)

@app.route("/search", methods=["GET"])
def search():
    query = request.args["query"]
    sql = "SELECT id, name, streetname, zip, phonenumber FROM restaurants WHERE name LIKE :query AND ishidden=0"
    result = db.session.execute(sql,{"query":"%"+query+"%"})
    resultToDisplay = result.fetchall()
    flash('We found the following restaurants:')
    return render_template("index.html", resultToDisplay = resultToDisplay)

@app.route("/contact-us")
def contactUs():

    return render_template("contact-us.html")

@app.route("/join-us")
def joinUs():

    return render_template("join-us.html")


@app.route("/new-account", methods=["POST"])
def newAccount():
    email = request.form["email"]
    hash_password = generate_password_hash(request.form["password"])
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    phonenumber = request.form["phonenumber"]
    streetname = request.form["streetname"]
    zip = request.form["zip"]


    sql = "INSERT INTO customers (email, firstname, lastname, phonenumber, streetname, zip, password) VALUES (:email, :firstname, :lastname, :phonenumber, :streetname, :zip, :hash_password)"
    db.session.execute(sql,{"email":email, "firstname":firstname, "lastname":lastname, "phonenumber":phonenumber, "streetname":streetname, "zip":zip, "hash_password":hash_password})
    db.session.commit()
    return redirect("/")

@app.route("/new-company", methods=["POST"])
def newCompany():
    companyname = request.form["company-name"]
    email = request.form["email"]
    hash_password = generate_password_hash(request.form["password"])
    businessid = request.form["business-id"]
    streetadress = request.form["streetadress"]
    zip = request.form["zip"]
    contactname = request.form["contact-name"]
    contactnumber = request.form["contact-number"]
    sql = "INSERT INTO companys (email, name, businessid, contactname, contactnumber, streetname, zip, password) VALUES (:email, :companyname, :businessid, :contactname, :contactnumber, :streetname, :zip, :hash_password)"
    db.session.execute(sql,{"email":email, "companyname":companyname, "businessid":businessid, "contactname":contactname, "contactnumber":contactnumber, "streetname":streetadress, "zip":zip, "hash_password":hash_password})
    db.session.commit()
    return redirect("/")

    


@app.route("/login")
def login():

    return render_template("login.html")

@app.route("/login-execute-customer",methods=["POST"])
def loginCustomer():

    username = request.form["email"]
    password = request.form["password"]

    sql = "SELECT password FROM customers WHERE email=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if user == None:
        flash('Login failed: Invalid username or password. (username not found)')
        return redirect("/login")
  
    else:
        hash_value = user[0]
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["type"] = "customer"
            return redirect("/")
        else:
            flash('Login failed: Invalid username or password. (password wrong)')
            return redirect("/login")

@app.route("/business-portal")
def businessPortal():
    return render_template("business-portal.html")



@app.route("/login-execute-business",methods=["POST"])
def loginBusiness():

    username = request.form["email"]
    password = request.form["password"]

    sql = "SELECT password FROM companys WHERE email=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if user == None:
        flash('Login failed: Invalid username or password. (username not found)')
        return redirect("/business-portal")

    else:
        hash_value = user[0]
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["type"] = "company"
            return redirect("/business-portal")
        else:
            flash('Login failed: Invalid username or password. (password wrong)')
            return redirect("/login")


    

@app.route("/manage-restaurants")
def manageRestaurants():

    username = session["username"]
    sqlGetId = "SELECT id FROM companys WHERE email=:username"
    resultId = db.session.execute(sqlGetId, {"username":username})
    ownerid = resultId.fetchone()[0]

    sqlGetRestaurants = db.session.execute("SELECT id, name FROM restaurants WHERE ownerid=:ownerid AND ishidden=0", {"ownerid":ownerid})
    restaurantsToDisplay = sqlGetRestaurants.fetchall()

    return render_template("/manage-restaurants.html", restaurantsToDisplay=restaurantsToDisplay)

@app.route("/add-restaurant", methods=["POST"])
def addRestaurants():

    username = session["username"]
    sqlGetId = "SELECT id FROM companys WHERE email=:username"
    resultId = db.session.execute(sqlGetId, {"username":username})
    ownerid = resultId.fetchone()[0]

    name = request.form["name"]
    email = request.form["email"]
    phonenumber = request.form["phonenumber"]
    streetadress = request.form["streetadress"]
    zip = request.form["zip"]

    sql = "INSERT INTO restaurants (name, email, phonenumber, streetname, zip, ownerid) VALUES (:name, :email, :phonenumber, :streetadress, :zip, :ownerid)"    
    db.session.execute(sql,{"name":name,"email":email,"phonenumber":phonenumber,"streetadress":streetadress, "zip":zip, "ownerid":ownerid})
    db.session.commit()

    flash('Restaurant added succsesfully')

    return redirect("/manage-restaurants")

@app.route("/restaurants/<int:id>")
def restaurants(id):

    sql = "SELECT name, email, phonenumber, streetname, zip FROM restaurants WHERE id=:id"
    result = db.session.execute(sql,{"id":id})
    restaurantsResult = result.fetchall()

    sql = "SELECT reviewerid, score, commentary FROM reviews WHERE restaurantid=:id"
    result = db.session.execute(sql,{"id":id})
    reviewersResult = result.fetchall()


    return render_template("/restaurants.html", id=id, restaurantsResult=restaurantsResult, reviewersResult=reviewersResult)



@app.route("/logout")
def logout():

    del session["type"]
    del session["username"]

    return redirect("/")


@app.route("/change-password")
def changePassword():
    return render_template("/change-password.html")


@app.route("/update-password", methods=["POST"])
def updatePassword():
    email = request.form["email"]
    hash_password = generate_password_hash(request.form["password"])
 

    sql = "UPDATE customers SET password =:hash_password WHERE email=:email"
    db.session.execute(sql,{"email":email, "hash_password":hash_password})



    db.session.commit()
    return redirect("/login")





