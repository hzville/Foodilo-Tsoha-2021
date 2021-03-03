from flask import Flask, render_template, redirect, render_template, request, session, flash
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
import xlrd
from random import *
from app import app
from db import db
import search, insert_into, select_from, login 

#start-pg.sh

app.secret_key = getenv("SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search_restaurants():
    query = request.args["query"]

    if str(query) == "":
        flash("Please enter a keyword")
        return render_template("index.html")

    result_to_display = search.get_restaurants(query)

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

    result = insert_into.add_new_customer(email, firstname, lastname, hash_password)
    
    if result:
        flash("Account " +str(email)+ " was created succesfully!")
        return redirect("/login")
    else:
        flash("Account " +str(email)+ " already exists, please use another email to create a account")
        return redirect("/join-us")

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

    result = insert_into.add_new_company(companyname,email,hash_password,business_id,streetadress,zip,contactname,contactnumber)

    if result:
        flash("Account " + str(email) +" was created succesfully!")
        return redirect("/login")
    else:
        flash("Account " +str(email)+ " already exists, please use another email to create a account")    
        return redirect("/join-us")
    

@app.route("/login")
def login_html():

    return render_template("login.html")

@app.route("/login-execute-customer",methods=["POST"])
def login_customer():

    username = request.form["email"]
    password = request.form["password"]

    if not username or not password:
        flash("Please fill in all the fields")
        return redirect("/login")

    result = login.customer_login(username, password)   
    
    if result:
        session["username"] = username
        session["type"] = "customer"
        return redirect("/")

    else:
        flash('Login failed: Invalid username or password.')
        return redirect("/login")
    

@app.route("/business-portal")
def business_portal():
    return render_template("business-portal.html")



@app.route("/login-execute-business",methods=["POST"])
def login_business():

    username = request.form["email"]
    password = request.form["password"]

    if not username or not password:
        flash("Please fill in all the fields")
        return redirect("/login")

    result = login.business_login(username, password)    

    if result:
        session["username"] = username
        session["type"] = "company"
        return redirect("/business-portal")

    else:
        flash('Login failed: Invalid username or password.')
        return redirect("/login")
        

    

@app.route("/manage-restaurants")
def manage_restaurants():

    if session.get("username") == None or session.get("type") != "company":
        flash('You need a business acocunt to manage restaurants')
        return render_template("/error.html")
    else:

        result, restaurants_to_display = select_from.get_owner_restaurants(session["username"])

        if result:

            return render_template("/manage-restaurants.html", restaurants_to_display=restaurants_to_display)
    
        else:
            flash('You need a business acocunt to manage restaurants')
            return render_template("/error.html")
  

@app.route("/add-restaurant", methods=["POST"])
def add_restaurants():

    print(session.get("username"))
    print("session.get(username) printed ^")

    if not session.get("username"):

        flash("Please login to add restaurants")
        redirect("/login")

    else: 

        username = session["username"]
        
        owner_id = select_from.get_owner_id(username)

        name = request.form["name"]
        email = request.form["email"]
        phonenumber = request.form["phonenumber"]
        streetadress = request.form["streetadress"]
        zip = request.form["zip"]
        
        zip_2, city = select_from.check_zip(zip)

        if not zip_2:
            flash("Zip code invalid, please try again.")
            return redirect("/manage-restaurants")

        insert_into.add_new_restaurant(name, email, phonenumber, streetadress, zip, city, owner_id)

        flash('Restaurant added succsesfully')

        return redirect("/manage-restaurants")

@app.route("/restaurants/<int:id>")
def restaurants(id):

    result, restaurant_result = select_from.get_restaurant_info(id)

    if not result:
        flash("Restaurant not found, please try again!")
        return render_template("error.html")

    else: 
        reviewers_result = select_from.get_restaurant_reviews(id)
        return render_template("/restaurants.html", id=id, restaurant_result=restaurant_result, reviewers_result=reviewers_result)

@app.route("/write-review/<int:restaurant_id>")
def write_review(restaurant_id):

    if session.get("username") is None:
        flash('Please login to write a review!')
        return render_template("/error.html")

    user = session["username"]

    customer_result, customer_id = select_from.get_customer_id(user)

    if not customer_result:
        flash("You need a customer account to write reviews")
        return render_template("error.html")
    else:

        result, review = select_from.get_customer_reviews(restaurant_id, customer_id)

    if result:
        return render_template("/write-review.html", review_history=review)

    else:
        result, restaurant_info = select_from.get_restaurant_info(restaurant_id)

        if result:
            return render_template("/write-review.html", restaurant_id = restaurant_id, restaurant_info=restaurant_info)
        
        else: 
            flash("Restaurant not found, please try again!")
            return render_template("/error.html")

@app.route("/review-execute", methods=["POST"])
def review_exceute():

    commentary = request.form["commentary"]
    score = request.form["rating"]
    restaurant_id = request.form["restaurant_id"]

    user = session["username"]

    result, customer_info = select_from.get_customer_info(user)
    if not result:
        flash("Oh no, there was a problem getting account details")
        return render_template("error.html")
    else:
        reviewer_id = customer_info[0]
        firstname = customer_info[2]
        lastname = customer_info[3]

    insert_into.add_new_review(restaurant_id,reviewer_id,firstname,lastname,score,commentary)

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