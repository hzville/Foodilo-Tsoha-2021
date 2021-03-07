from db import db


def get_owner_restaurants(username):

    sql_get_id = "SELECT id FROM companys WHERE email=:username"
    result_id = db.session.execute(sql_get_id, {"username": username})
    owner_id = result_id.fetchone()

    if owner_id != None:

        sql_get_restaurants = db.session.execute(
            "SELECT id, name FROM restaurants WHERE owner_id=:owner_id AND is_hidden=false", {"owner_id": owner_id[0]})
        restaurants_to_display = sql_get_restaurants.fetchall()

        return True, restaurants_to_display

    else:
        return False, 0


def get_owner_id(username):

    sqlGetId = "SELECT id FROM companys WHERE email=:username"
    resultId = db.session.execute(sqlGetId, {"username": username})
    owner_id = resultId.fetchone()[0]

    return owner_id


def check_zip(zip):
    sql = "SELECT city FROM postnumber_mapping WHERE postnumber=:zip"
    result = db.session.execute(sql, {"zip": zip})
    city = result.fetchone()

    if city == None:
        return False, 0
    else:
        return True, city[0]


def get_restaurant_info(id):

    sql = "SELECT name, email, phonenumber, streetname, zip, city, is_hidden, owner_id FROM restaurants WHERE id=:id AND is_hidden = False"
    result = db.session.execute(sql, {"id": id})
    restaurant_result = result.fetchall()

    if len(restaurant_result) <= 0:
        return False, 0

    else:
        return True, restaurant_result


def get_restaurant_reviews(id):

    sql = "SELECT reviewer_firstname, reviewer_lastname, score, commentary FROM reviews WHERE is_hidden = false AND restaurant_id=:id ORDER BY id DESC"
    result = db.session.execute(sql, {"id": id})
    reviewers_result = result.fetchall()

    return reviewers_result


def get_latest_reviews():

    result = db.session.execute("SELECT reviews.restaurant_id, reviewer_firstname, reviewer_lastname, restaurant_name, score, commentary FROM restaurants, reviews WHERE reviews.is_hidden = false AND restaurants.is_hidden = false AND reviews.restaurant_id = restaurants.id ORDER BY reviews.id DESC LIMIT 5;")
    latest_result = result.fetchall()
    return latest_result


def get_most_reviews():

    result = db.session.execute("SELECT restaurant_name, restaurant_id, COUNT(restaurant_id) AS reviews_pcs FROM reviews, restaurants WHERE reviews.is_hidden = false AND restaurants.is_hidden = false AND reviews.restaurant_id = restaurants.id GROUP BY restaurant_id, restaurant_name ORDER BY reviews_pcs DESC LIMIT 5")
    most_reviews = result.fetchall()
    return most_reviews


def get_best_avg():

    result = db.session.execute("SELECT restaurant_name,restaurant_id, AVG(score) AS avg_stars, COUNT(restaurant_id) AS reviews_pcs FROM reviews, restaurants WHERE reviews.is_hidden = false AND restaurants.is_hidden = false AND reviews.restaurant_id = restaurants.id GROUP BY restaurant_id, restaurant_name ORDER BY avg_stars DESC LIMIT 5")
    best_avg = result.fetchall()

    return best_avg


def get_restaurant_score(id):

    sql = "SELECT COUNT(*), SUM(score) FROM reviews WHERE restaurant_id=:id"
    result = db.session.execute(sql, {"id": id})
    result2 = result.fetchall()

    print(result2)

    return


def get_customer_id(username):

    sql = "SELECT id FROM customers WHERE email=:username"
    result = db.session.execute(sql, {"username": username})
    customer_id = result.fetchone()

    if customer_id == None:
        return False, 0
    else:
        return True, customer_id[0]


def get_customer_info(username):

    sql = "SELECT id, email, firstname, lastname FROM customers WHERE email=:user"
    result = db.session.execute(sql, {"user": username})
    customer_info = result.fetchone()

    if customer_info == None:
        return False, 0
    else:
        return True, customer_info


def get_customer_reviews(restaurant_id, customer_id):

    sql = "SELECT commentary, score, restaurant_id FROM reviews WHERE restaurant_id=:restaurant_id AND reviewer_id=:reviewer_id AND is_hidden = false"
    result = db.session.execute(
        sql, {"restaurant_id": restaurant_id, "reviewer_id": customer_id})
    review_history = result.fetchall()

    if len(review_history) > 0:
        return True, review_history

    else:
        return False, 0


def get_customer_all_reviews(id):
    sql = "SELECT reviews.restaurant_id, reviews.restaurant_name, reviews.datemade, reviews.score, reviews.commentary FROM reviews, restaurants WHERE reviewer_id=:reviewer_id AND reviews.is_hidden = false AND restaurants.is_hidden = false AND reviews.restaurant_id = restaurants.id"
    result = db.session.execute(sql, {"reviewer_id": id})
    review_history = result.fetchall()
    return review_history


def check_if_hidden_customer(username):

    sql = "SELECT is_hidden FROM customers WHERE email=:email"
    result = db.session.execute(sql, {"email": username})
    is_hidden = result.fetchone()

    if is_hidden == None:
        return False

    if not is_hidden[0]:
        return False
    else:
        return True


def check_if_hidden_company(username):

    sql = "SELECT is_hidden FROM companys WHERE email=:email"
    result = db.session.execute(sql, {"email": username})
    is_hidden = result.fetchone()

    if is_hidden == None:
        return False

    if not is_hidden[0]:
        return False
    else:
        return True


def check_if_admin(username):

    sql = "SELECT is_admin FROM customers WHERE email=:email"
    result = db.session.execute(sql, {"email": username})
    is_admin = result.fetchone()

    if is_admin == None:
        return False

    if is_admin[0]:
        return True
    else:
        return False


def get_feedback_waiting_action():

    result = db.session.execute(
        "SELECT * FROM feedback WHERE waiting_action = true")
    feedback = result.fetchall()
    return feedback


def get_feeback_resolved():

    result = db.session.execute(
        "SELECT * FROM feedback WHERE waiting_action = false")
    feedback = result.fetchall()
    return feedback
