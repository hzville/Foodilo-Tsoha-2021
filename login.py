from db import db
from werkzeug.security import check_password_hash, generate_password_hash


def customer_login(username, password):
    
    sql = "SELECT password FROM customers WHERE email=:username"
    result = db.session.execute(sql, {"username":username})
    query_result = result.fetchone()
    
    return password_auth(username, password, query_result)



def business_login(username, password):

    sql = "SELECT password FROM companys WHERE email=:username"
    result = db.session.execute(sql, {"username":username})
    query_result = result.fetchone()
   
    return password_auth(username, password, query_result)


def password_auth(usename, password, query_result):

    if query_result == None:
        return False

    else:
        hash_value = query_result[0]

        if check_password_hash(hash_value, password):
            return True

        else:
            return False
  

