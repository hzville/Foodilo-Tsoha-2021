from db import db

def add_new_customer(email, firstname, lastname, hash_password):

    sql = "SELECT * FROM customers WHERE email=:email"
    db_query = db.session.execute(sql,{"email":email})
    result = db_query.fetchone()


    if result != None:
        return False

    else:
        sql = "INSERT INTO customers (email, firstname, lastname, password) VALUES (:email, :firstname, :lastname, :hash_password)"
        db.session.execute(sql,{"email":email, "firstname":firstname, "lastname":lastname, "hash_password":hash_password})
        db.session.commit()

        return True

def add_new_company(companyname,email,hash_password,business_id,streetadress,zip,contactname,contactnumber):

    sql = "SELECT * FROM companys WHERE email=:email"
    db_query = db.session.execute(sql,{"email":email})
    result = db_query.fetchone()

    print(result)

    if result != None:
        
        return False

    else:
        
        sql = "INSERT INTO companys (email, name, business_id, contactname, contactnumber, streetname, zip, password) VALUES (:email, :companyname, :business_id, :contactname, :contactnumber, :streetname, :zip, :hash_password)"
        db.session.execute(sql,{"email":email, "companyname":companyname, "business_id":business_id, "contactname":contactname, "contactnumber":contactnumber, "streetname":streetadress, "zip":zip, "hash_password":hash_password})
        db.session.commit()     

        return True  


def add_new_restaurant(name, email, phonenumber, streetadress, zip, city, owner_id):
    sql = "INSERT INTO restaurants (name, email, phonenumber, streetname, zip, city, owner_id) VALUES (:name, :email, :phonenumber, :streetadress, :zip, :city, :owner_id)"    
    db.session.execute(sql,{"name":name,"email":email,"phonenumber":phonenumber,"streetadress":streetadress, "zip":zip, "city":city, "owner_id":owner_id})
    db.session.commit()

def add_new_review(restaurant_id,reviewer_id,firstname,lastname,score,commentary):
    sql = "INSERT INTO reviews (restaurant_id, reviewer_id, reviewer_firstname, reviewer_lastname, score, commentary) VALUES (:restaurant_id, :reviewer_id, :reviewer_firstname, :reviewer_lastname, :score, :commentary)"
    db.session.execute(sql,{"restaurant_id":restaurant_id, "reviewer_id":reviewer_id, "reviewer_firstname":firstname, "reviewer_lastname":lastname, "score":score, "commentary":commentary})
    db.session.commit()