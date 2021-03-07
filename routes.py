from flask import Flask, render_template, redirect, render_template, request, session, flash
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
import xlrd
from random import *
from app import app
from db import db
import search
import insert_into
import select_from
import login
import update_table


app.secret_key = getenv("SECRET_KEY")


@app.route("/")
def index():

    latest_reviews = select_from.get_latest_reviews()
    most_reviews = select_from.get_most_reviews()
    best_avg = select_from.get_best_avg()

    return render_template("index.html", best_avg=best_avg, most_reviews=most_reviews, latest_reviews=latest_reviews)


@app.route("/search", methods=["GET"])
def search_restaurants():
    query = request.args["query"]

    latest_reviews = select_from.get_latest_reviews()
    most_reviews = select_from.get_most_reviews()
    best_avg = select_from.get_best_avg()

    if str(query) == "":
        flash("Please enter a keyword")
        return render_template("index.html", best_avg=best_avg, most_reviews=most_reviews, latest_reviews=latest_reviews)
    result_to_display = search.get_restaurants(query)

    if len(result_to_display) <= 0:
        flash("No restaurants was found with the query " + str(query))
        return render_template("index.html", best_avg=best_avg, most_reviews=most_reviews, latest_reviews=latest_reviews)

    return render_template("index.html", result_to_display=result_to_display, best_avg=best_avg, most_reviews=most_reviews, latest_reviews=latest_reviews)


@app.route("/contact-us")
def contact_us():

    if session.get("username"):
        return render_template("contact-us.html", email=session["username"])
    else:
        return render_template("contact-us.html")


@app.route("/join-us")
def join_us():

    return render_template("join-us.html")


@app.route("/new-account", methods=["POST"])
def new_account():
    email = request.form["email"].lower()
    hash_password = generate_password_hash(request.form["password"])
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]

    result = insert_into.add_new_customer(
        email, firstname, lastname, hash_password)

    if result:
        flash("Account " + str(email) + " was created succesfully!")
        return redirect("/login")
    else:
        flash("Account " + str(email) +
              " already exists, please use another email to create a account")
        return redirect("/join-us")


@app.route("/new-company", methods=["POST"])
def new_company():
    companyname = request.form["company-name"]
    email = request.form["email"].lower()
    hash_password = generate_password_hash(request.form["password"])
    business_id = request.form["business-id"]
    streetadress = request.form["streetadress"]
    zip = request.form["zip"]
    contactname = request.form["contact-name"]
    contactnumber = request.form["contact-number"]

    result = insert_into.add_new_company(
        companyname, email, hash_password, business_id, streetadress, zip, contactname, contactnumber)

    if result:
        flash("Account " + str(email) + " was created succesfully!")
        return redirect("/login")
    else:
        flash("Account " + str(email) +
              " already exists, please use another email to create a account")
        return redirect("/join-us")


@app.route("/login")
def login_html():

    return render_template("login.html")


@app.route("/login-execute-customer", methods=["POST"])
def login_customer():

    username = request.form["email"].lower()
    password = request.form["password"]

    if not username or not password:
        flash("Please fill in all the fields")
        return redirect("/login")

    check_if_hidden = select_from.check_if_hidden_customer(username)

    if check_if_hidden:
        flash("Account disabled, please contact support")
        return redirect("/login")

    result = login.customer_login(username, password)

    if result:

        is_admin = select_from.check_if_admin(username)

        if not is_admin:
            session["username"] = username
            session["type"] = "customer"
            result, customer_id = select_from.get_customer_id(username)
            session["id"] = customer_id

            return redirect("/")

        else:
            session["username"] = username
            session["type"] = "admin"
            result, customer_id = select_from.get_customer_id(username)
            session["id"] = customer_id
            print(session["username"])
            print(session["id"])
            return redirect("/")

    else:
        flash('Login failed: Invalid username or password.')
        return redirect("/login")


@app.route("/business-portal")
def business_portal():
    return render_template("business-portal.html")


@app.route("/login-execute-business", methods=["POST"])
def login_business():

    username = request.form["email"].lower()
    password = request.form["password"]

    if not username or not password:
        flash("Please fill in all the fields")
        return redirect("/login")

    check_if_hidden = select_from.check_if_hidden_company(username)

    if check_if_hidden:
        flash("Account disabled, please contact support")
        return redirect("/login")

    result = login.business_login(username, password)

    if result:
        session["username"] = username
        session["type"] = "company"
        session["id"] = select_from.get_owner_id(username)
        return redirect("/business-portal")

    else:
        flash('Login failed: Invalid username or password.')
        return redirect("/login")


@app.route("/manage-account", methods=["POST", "GET"])
def manage_account():

    if not session.get("username"):
        flash("You need to login to manage account settings")
        return render_template("/error.html")

    review_history = select_from.get_customer_all_reviews(session["id"])

    if 'update-pw' in request.form:
        first_input = request.form["first-input-pwupdate"]
        second_input = request.form["second-input-pwupdate"]

        if first_input != second_input:
            flash("Passwords dont match, please try again")
            return redirect("/manage-account")
        else:
            if session.get("type") == 'customer' or session.get("type") == 'admin':
                update_table.update_password_customer(
                    session.get("id"), generate_password_hash(first_input))
                flash("Password updated!")
                return render_template("/manage-account.html", review_history=review_history)
            elif session.get("type") == 'company':
                update_table.update_password_company(
                    session.get("id"), generate_password_hash(first_input))
                flash("Password updated!")
                return render_template("/manage-account.html")
            else:
                flash("There was a problem updating the password, please try again.")
                return render_template("/manage-account.html")

    if session.get("type") == "customer":
        review_history = select_from.get_customer_all_reviews(session["id"])
        return render_template("/manage-account.html", review_history=review_history)

    return render_template("/manage-account.html")


@app.route("/manage-restaurants", methods=['GET', 'POST'])
def manage_restaurants():

    if session.get("username") == None or session.get("type") != "company":
        flash('You need a business acocunt to manage restaurants')
        return render_template("/error.html")
    else:

        result, restaurants_to_display = select_from.get_owner_restaurants(
            session["username"])

        if 'edit' in request.form:
            restaurant_id = request.form["restaurant_id"]
            result, restaurant_info = select_from.get_restaurant_info(
                restaurant_id)
            return render_template("/manage-restaurants.html", restaurant_to_edit=restaurant_info, restaurant_id=restaurant_id)

        if 'delete-first' in request.form:
            restaurant_id = request.form["restaurant_id"]
            result, restaurant_info = select_from.get_restaurant_info(
                restaurant_id)
            return render_template("/manage-restaurants.html", restaurant_to_delete=restaurant_info, restaurant_id=restaurant_id)

        if 'delete' in request.form:
            restaurant_id = request.form["restaurant_id"]
            update_table.set_restaurant_hidden(
                restaurant_id, session.get("id"))
            flash("Restaurant deleted!")
            return redirect("/manage-restaurants")

        if result:

            return render_template("/manage-restaurants.html", restaurants_to_display=restaurants_to_display)

        else:
            flash('You need a business acocunt to manage restaurants')
            return render_template("/error.html")


@app.route("/add-restaurant", methods=["POST"])
def add_restaurants():
    print("made it to add_restauratsn")

    if not session.get("username"):

        flash("Please login to add restaurants")
        redirect("/login")

    else:

        username = session["username"]
        owner_id = session["id"]
        name = request.form["name"]
        email = request.form["email"]
        phonenumber = request.form["phonenumber"]
        streetadress = request.form["streetadress"]
        zip = request.form["zip"]

        zip_2, city = select_from.check_zip(zip)

        if not zip_2:
            flash("Zip code invalid, please try again.")
            return render_template("/manage-restaurants.html", name=name, email=email, phonenumber=phonenumber, streetadress=streetadress)

        if 'update' in request.form:
            print("made it to the upadte form")
            print(request.form["restaurant_id"])
            result, restaurant_info = select_from.get_restaurant_info(
                request.form["restaurant_id"])

            # Checks restaurants table owner_id value
            if restaurant_info[0][7] == owner_id:
                print(request.form["restaurant_id"], name,
                      email, phonenumber, streetadress, zip, city)
                update_table.update_restaurant_info(
                    request.form["restaurant_id"], name, email, phonenumber, streetadress, zip, city)
                flash("Restaurant data updated!")
                return redirect("/manage-restaurants")
            else:
                flash("You need to be owner of restaurant to update data")
                return redirect("/")

            
            return redirect("/")

        insert_into.add_new_restaurant(
            name, email, phonenumber, streetadress, zip, city, owner_id)

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
        query = select_from.get_restaurant_score(id)

        return render_template("/restaurants.html", id=id, restaurant_result=restaurant_result, reviewers_result=reviewers_result)


@app.route("/write-review/<int:restaurant_id>", methods=['GET', 'POST'])
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

        result, review = select_from.get_customer_reviews(
            restaurant_id, customer_id)

        if 'edit' in request.form:
            result, restaurant_info = select_from.get_restaurant_info(
                restaurant_id)
            return render_template("/write-review.html", restaurant_id=restaurant_id, restaurant_info=restaurant_info, commentary=review[0][0], score=review[0][1])

        elif 'delete' in request.form:
            update_table.set_review_hidden(restaurant_id, customer_id)
            flash("Review deleted!")
            return redirect("/write-review/"+str(restaurant_id))

    if result:
        return render_template("/write-review.html", review_history=review)

    else:
        result, restaurant_info = select_from.get_restaurant_info(
            restaurant_id)

        if result:
            return render_template("/write-review.html", restaurant_id=restaurant_id, restaurant_info=restaurant_info)

        else:
            flash("Restaurant not found, please try again!")
            return render_template("/error.html")


@app.route("/review-execute", methods=["POST"])
def review_exceute():

    commentary = request.form["commentary"]
    score = request.form["rating"]
    restaurant_id = request.form["restaurant_id"]
    restaurant_name = request.form["restaurant_name"]

    user = session["username"]

    result, customer_info = select_from.get_customer_info(user)
    if not result:
        flash("Oh no, there was a problem getting account details")
        return render_template("error.html")
    else:
        reviewer_id = customer_info[0]
        firstname = customer_info[2]
        lastname = customer_info[3]

    check_if_update, review = select_from.get_customer_reviews(
        restaurant_id, reviewer_id)

    if check_if_update:
        update_table.update_review(
            restaurant_id, reviewer_id, commentary, score)
        flash("Review updated!")
        return redirect("/write-review/"+str(restaurant_id))
    else:

        insert_into.add_new_review(
            restaurant_id, restaurant_name, reviewer_id, firstname, lastname, score, commentary)

        flash("Review submitted successfully!")

        return redirect("/restaurants/"+str(restaurant_id))


@app.route("/logout")
def logout():

    del session["type"]
    del session["username"]
    del session["id"]
    return redirect("/")


@app.route("/send-feedback", methods=["POST"])
def send_feedback():

    name = request.form["name"]
    email = request.form["email"]
    feedback = request.form["feedback"]

    insert_into.add_new_feedback(name, email, feedback)

    flash("Thank you for your feedback. We handle it as soon as posssible!")
    return redirect("/")


@app.route("/admin-console", methods=["POST", "GET"])
def admin_console():

    if session.get("type") == 'admin':

        if 'manage-customer-accounts' in request.form:
            query = request.form["search"]

            return render_template("/admin-console.html", customer_result=search.get_customers(query), company_result=search.get_company(query), review_result=search.get_reviews(query))

        if 'show-feedback' in request.form:
            return render_template("/admin-console.html", feedback_waiting=select_from.get_feedback_waiting_action(), feedback_resolved=select_from.get_feeback_resolved())

        if 'make-admin' in request.form:
            email = request.form["customer_email"]
            update_table.make_admin(email)
            flash(email + " is now admin")
            return render_template("/admin-console.html", customer_result=search.get_customers(email))

        if 'remove-admin' in request.form:
            email = request.form["customer_email"]
            update_table.remove_admin(email)
            flash("Admin status has been removed from " + email)
            return render_template("/admin-console.html", customer_result=search.get_customers(email))

        if 'enable-customer' in request.form:
            email = request.form["customer_email"]
            update_table.enable_customer(email)
            flash("Customer account " + email + " has been enabled")
            return render_template("/admin-console.html", customer_result=search.get_customers(email))

        if 'disable-customer' in request.form:
            email = request.form["customer_email"]
            update_table.disable_customer(email)
            flash("Customer account " + email + " has been disabled")
            return render_template("/admin-console.html", customer_result=search.get_customers(email))

        if 'enable-company' in request.form:
            email = request.form["company_email"]
            update_table.enable_company(email)
            flash("Company account " + email + " has been enabled")
            return render_template("/admin-console.html", company_result=search.get_company(email))

        if 'disable-company' in request.form:
            email = request.form["company_email"]
            update_table.disable_company(email)
            flash("Company account " + email + " has been disabled")
            return render_template("/admin-console.html", company_result=search.get_company(email))

        if 'recover-review' in request.form:
            id = request.form["review_id"]
            update_table.recover_review(id)
            flash("Review id " + id + " has been recovered")
            return render_template("/admin-console.html", review_result=search.get_reviews(""))

        if 'delete-review' in request.form:
            id = request.form["review_id"]
            update_table.delete_review(id)
            flash("Review id " + id + " has been deleted")
            return render_template("/admin-console.html", review_result=search.get_reviews(""))

        if 'mark-resolved' in request.form:
            update_table.set_feedback_resolved(request.form["feedback-id"])
            flash("Feedback marked as resolved")
            return render_template("/admin-console.html", feedback_waiting=select_from.get_feedback_waiting_action(), feedback_resolved=select_from.get_feeback_resolved())

        if 'needs-action' in request.form:
            update_table.set_feedback_needs_action(request.form["feedback-id"])
            flash("Feedback marked as needs action")
            return render_template("/admin-console.html", feedback_waiting=select_from.get_feedback_waiting_action(), feedback_resolved=select_from.get_feeback_resolved())

    return render_template("/admin-console.html")


# Use this for reading excel into database

# @app.route("/read")
def read():

    path = "zip_code_mapping.xls"

    excel_workbook = xlrd.open_workbook(path)
    excel_worksheet = excel_workbook.sheet_by_index(0)
    how_many = 0

    for x in range(0, excel_worksheet.nrows):

        postinumero = excel_worksheet.cell_value(x, 0)
        kaupunki = excel_worksheet.cell_value(x, 1)

        sql = "INSERT INTO postnumber_mapping (postnumber, city) VALUES (:postinumero, :kaupunki)"
        db.session.execute(
            sql, {"postinumero": postinumero, "kaupunki": kaupunki})
        how_many += 1

    db.session.commit()

    flash("Execute successfull, inserted rows " + str(how_many))
    return render_template("index.html")

