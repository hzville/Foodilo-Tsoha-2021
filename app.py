from flask import Flask, render_template, redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
import xlrd
from random import *

#start-pg.sh

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search():
    query = request.args["query"]

    if str(query) == "":
        flash("Please enter a keyword")
        return render_template("index.html")

    sql = "SELECT id, name, streetname, zip, city, phonenumber FROM restaurants WHERE is_hidden=false AND name ILIKE :query OR city ILIKE :query"
    result = db.session.execute(sql,{"query":"%"+query+"%"})
    result_to_display = result.fetchall()

    if len(result_to_display) <= 0:
        flash("No restaurants was found with the query " + str(query))
        return render_template("index.html")

    return render_template("index.html", result_to_display = result_to_display,)

@app.route("/contact-us")
def contact_us():

    return render_template("contact-us.html")

@app.route("/join-us")
def join_us():

    return render_template("join-us.html")


@app.route("/new-account", methods=["POST"])
def new_account():
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
    flash('Account created succesfully')
    return redirect("/login")

@app.route("/new-company", methods=["POST"])
def new_company():
    companyname = request.form["company-name"]
    email = request.form["email"]
    hash_password = generate_password_hash(request.form["password"])
    business_id = request.form["business-id"]
    streetadress = request.form["streetadress"]
    zip = request.form["zip"]
    contactname = request.form["contact-name"]
    contactnumber = request.form["contact-number"]
    sql = "INSERT INTO companys (email, name, business_id, contactname, contactnumber, streetname, zip, password) VALUES (:email, :companyname, :business_id, :contactname, :contactnumber, :streetname, :zip, :hash_password)"
    db.session.execute(sql,{"email":email, "companyname":companyname, "business_id":business_id, "contactname":contactname, "contactnumber":contactnumber, "streetname":streetadress, "zip":zip, "hash_password":hash_password})
    db.session.commit()


    return redirect("/")

    

@app.route("/login")
def login():

    return render_template("login.html")

@app.route("/login-execute-customer",methods=["POST"])
def login_customer():

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
            print(session["username"])
            return redirect("/")
        else:
            flash('Login failed: Invalid username or password. (password wrong)')
            return redirect("/login")

@app.route("/business-portal")
def business_portal():
    return render_template("business-portal.html")



@app.route("/login-execute-business",methods=["POST"])
def login_business():

    username = request.form["email"]
    password = request.form["password"]

    sql = "SELECT password FROM companys WHERE email=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if user == None:
        flash('Login failed: Invalid username or password. (username not found)')
        return redirect("/login")

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
def manage_restaurants():

    if session.get("username") is None:
        flash('You need a business acocunt to manage restaurants')
        return render_template("/error.html")

    username = session["username"]
    sqlGetId = "SELECT id FROM companys WHERE email=:username"
    resultId = db.session.execute(sqlGetId, {"username":username})
    owner_id = resultId.fetchone()

    if owner_id != None:

        owner_id2 = owner_id[0]

        sqlGetRestaurants = db.session.execute("SELECT id, name FROM restaurants WHERE owner_id=:owner_id2 AND is_hidden=false", {"owner_id2":owner_id2})
        restaurantsToDisplay = sqlGetRestaurants.fetchall()

        return render_template("/manage-restaurants.html", restaurantsToDisplay=restaurantsToDisplay)
    else:
        flash('You need a business acocunt to manage restaurants')
        return render_template("/error.html")
  

@app.route("/add-restaurant", methods=["POST"])
def add_restaurants():

    username = session["username"]
    sqlGetId = "SELECT id FROM companys WHERE email=:username"
    resultId = db.session.execute(sqlGetId, {"username":username})
    owner_id = resultId.fetchone()[0]

    name = request.form["name"]
    email = request.form["email"]
    phonenumber = request.form["phonenumber"]
    streetadress = request.form["streetadress"]
    zip = request.form["zip"]
    
    sql= "SELECT city FROM postnumber_mapping WHERE postnumber=:zip"
    result = db.session.execute(sql, {"zip":zip})
    city1 = result.fetchone()

    if city1 == None:
        flash("Zip code invalid, please try again.")
        return redirect("/manage-restaurants")

    city = city1[0]
    sql = "INSERT INTO restaurants (name, email, phonenumber, streetname, zip, city, owner_id) VALUES (:name, :email, :phonenumber, :streetadress, :zip, :city, :owner_id)"    
    db.session.execute(sql,{"name":name,"email":email,"phonenumber":phonenumber,"streetadress":streetadress, "zip":zip, "city":city, "owner_id":owner_id})
    db.session.commit()

    flash('Restaurant added succsesfully')

    return redirect("/manage-restaurants")

@app.route("/restaurants/<int:id>")
def restaurants(id):

    sql = "SELECT name, email, phonenumber, streetname, zip FROM restaurants WHERE id=:id"
    result = db.session.execute(sql,{"id":id})
    restaurantsResult = result.fetchall()

    if len(restaurantsResult) <= 0:
        flash("Restaurant not found, please try again!")
        return render_template("error.html")

    sql = "SELECT reviewer_firstname, reviewer_lastname, score, commentary FROM reviews WHERE restaurant_id=:id"
    result = db.session.execute(sql,{"id":id})
    reviewersResult = result.fetchall()


    return render_template("/restaurants.html", id=id, restaurantsResult=restaurantsResult, reviewersResult=reviewersResult)

@app.route("/write-review/<int:id>")
def write_review(id):

    if session.get("username") is None:
        flash('Please login to write a review!')
        return render_template("/error.html")

    user = session["username"]
    sql= "SELECT id FROM customers WHERE email=:user"
    result = db.session.execute(sql, {"user":user})
    result2 = result.fetchone()
    reviewer_id = result2[0]

    sql = "SELECT commentary, score FROM reviews WHERE restaurant_id=:restaurant_id AND reviewerid=:reviewer_id"
    result = db.session.execute(sql, {"restaurant_id":id, "reviewer_id":reviewer_id})
    review_history = result.fetchall()

    if len(review_history) > 0:
        return render_template("/write-review.html", review_history=review_history)


    sql= "SELECT id, name, is_hidden FROM restaurants WHERE id=:id"
    result = db.session.execute(sql,{"id":id})
    restaurant_info = result.fetchall()

    if len(restaurant_info) <= 0:
        flash("Restaurant not found, please try again!")
        return render_template("/error.html")

    return render_template("/write-review.html", restaurant_info=restaurant_info)

@app.route("/review-execute", methods=["POST"])
def review_exceute():
    commentary = request.form["commentary"]
    score = request.form["rating"]
    restaurant_id = request.form["restaurant_id"]

    user = session["username"]
    sql = "SELECT id, firstname, lastname FROM customers WHERE email=:user"
    result = db.session.execute(sql,{"user":user})
    result2 = result.fetchone()
    reviewer_id = result2[0]
    firstname = result2[1]
    lastname = result2[2]

    sql = "INSERT INTO reviews (restaurant_id, reviewerid, reviewer_firstname, reviewer_lastname, score, commentary) VALUES (:restaurant_id, :reviewer_id, :reviewer_firstname, :reviewer_lastname, :score, :commentary)"
    db.session.execute(sql,{"restaurant_id":restaurant_id, "reviewer_id":reviewer_id, "reviewer_firstname":firstname, "reviewer_lastname":lastname, "score":score, "commentary":commentary})
    db.session.commit()

    flash("Review submitted successfully!")

    return redirect("/restaurants/"+str(restaurant_id))


@app.route("/logout")
def logout():

    del session["type"]
    del session["username"]

    return redirect("/")

# Use this for reading excel into database

#@app.route("/read")
def read():

    path = "zip_code_mapping.xls"

    excel_workbook = xlrd.open_workbook(path)
    excel_worksheet = excel_workbook.sheet_by_index(0)
    how_many = 0

    for x in range(0, excel_worksheet.nrows):

        postinumero = excel_worksheet.cell_value(x,0)
        kaupunki = excel_worksheet.cell_value(x,1)

        sql = "INSERT INTO postnumber_mapping (postnumber, city) VALUES (:postinumero, :kaupunki)"
        db.session.execute(sql,{"postinumero":postinumero, "kaupunki":kaupunki})
        how_many += 1

    db.session.commit()

    flash("Execute successfull, inserted rows "+ str(how_many))
    return render_template("index.html")

#@app.route("/change-password")
#def change_password():
#    return render_template("/change-password.html")


#@app.route("/update-password", methods=["POST"])
#def updatePassword():
#    email = request.form["email"]
#    hash_password = generate_password_hash(request.form["password"])
 

#    sql = "UPDATE customers SET password =:hash_password WHERE email=:email"
#    db.session.execute(sql,{"email":email, "hash_password":hash_password})



#    db.session.commit()
#    return redirect("/login")





