from db import db


def get_restaurants(query):
    sql = "SELECT id, name, streetname, zip, city, phonenumber FROM restaurants WHERE is_hidden=false AND name ILIKE :query OR city ILIKE :query AND is_hidden=false"
    result = db.session.execute(sql, {"query": "%"+query+"%"})
    result_to_return = result.fetchall()

    return result_to_return


def get_customers(query):
    sql = "SELECT id, email, firstname, lastname, singupdate, is_admin, is_hidden FROM customers WHERE email ILIKE :query OR firstname ILIKE :query OR lastname ILIKE :query"
    result = db.session.execute(sql, {"query": "%"+query+"%"})
    result_to_return = result.fetchall()

    return result_to_return


def get_company(query):
    sql = "SELECT id, email, name, singupdate, is_hidden FROM companys WHERE name ILIKE :query OR email ILIKE :query"
    result = db.session.execute(sql, {"query": "%"+query+"%"})
    result_to_return = result.fetchall()

    return result_to_return


def get_reviews(query):
    sql = "SELECT id, reviewer_id, reviewer_firstname, reviewer_lastname, datemade, score, commentary, is_hidden FROM reviews WHERE reviewer_firstname ILIKE :query OR reviewer_lastname ILIKE :query OR commentary ILIKE :query"
    result = db.session.execute(sql, {"query": "%"+query+"%"})
    result_to_return = result.fetchall()

    return result_to_return
