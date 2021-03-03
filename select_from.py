from db import db

def get_owner_restaurants(username):

    sql_get_id = "SELECT id FROM companys WHERE email=:username"
    result_id = db.session.execute(sql_get_id, {"username":username})
    owner_id = result_id.fetchone()

    if owner_id != None:

        sql_get_restaurants = db.session.execute("SELECT id, name FROM restaurants WHERE owner_id=:owner_id AND is_hidden=false", {"owner_id":owner_id[0]})
        restaurants_to_display = sql_get_restaurants.fetchall()

        return True, restaurants_to_display

    else:
        return False, 0

def get_owner_id(username):

    sqlGetId = "SELECT id FROM companys WHERE email=:username"
    resultId = db.session.execute(sqlGetId, {"username":username})
    owner_id = resultId.fetchone()[0]

    return owner_id

def check_zip(zip):
    sql= "SELECT city FROM postnumber_mapping WHERE postnumber=:zip"
    result = db.session.execute(sql, {"zip":zip})
    city = result.fetchone()

    if city == None:
        return False, 0
    else:
        return True, city[0]


def get_restaurant_info(id):

    sql = "SELECT name, email, phonenumber, streetname, zip, city, is_hidden FROM restaurants WHERE id=:id AND is_hidden = False"
    result = db.session.execute(sql,{"id":id})
    restaurant_result = result.fetchall()

    if len(restaurant_result) <= 0:
        return False, 0

    else:
        return True, restaurant_result

def get_restaurant_reviews(id):

    sql = "SELECT reviewer_firstname, reviewer_lastname, score, commentary FROM reviews WHERE restaurant_id=:id"
    result = db.session.execute(sql,{"id":id})
    reviewers_result = result.fetchall()

    return reviewers_result


def get_customer_id(username):

    sql= "SELECT id FROM customers WHERE email=:username"
    result = db.session.execute(sql, {"username":username})
    customer_id = result.fetchone()

    if customer_id == None:
        return False, 0
    else:
        return True, customer_id[0]

def get_customer_info(username):

    sql = "SELECT id, email, firstname, lastname FROM customers WHERE email=:user"
    result = db.session.execute(sql,{"user":username})
    customer_info = result.fetchone()
   
    if customer_info == None:
        return False, 0
    else:
        return True, customer_info



def get_customer_reviews(restaurant_id, customer_id):

    sql = "SELECT commentary, score FROM reviews WHERE restaurant_id=:restaurant_id AND reviewer_id=:reviewer_id"
    result = db.session.execute(sql, {"restaurant_id":restaurant_id, "reviewer_id":customer_id})
    review_history = result.fetchall()

    if len(review_history) > 0:
        return True, review_history
    
    else:
        return False, 0


