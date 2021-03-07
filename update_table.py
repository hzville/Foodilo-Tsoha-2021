from db import db

def update_review(restaurant_id, reviewer_id, commentary, score):

    sql = "UPDATE reviews SET commentary=:commentary, score =:score WHERE restaurant_id =:restaurant_id AND reviewer_id=:reviewer_id AND is_hidden = false"
    db.session.execute(sql,{"commentary":commentary, "score":score, "restaurant_id":restaurant_id, "reviewer_id":reviewer_id}) 
    db.session.commit()

def set_review_hidden(restaurant_id, reviewer_id):

    sql = "UPDATE reviews SET is_hidden= true WHERE restaurant_id=:restaurant_id AND reviewer_id=:reviewer_id"
    db.session.execute(sql,{"restaurant_id":restaurant_id, "reviewer_id":reviewer_id})
    db.session.commit()

def update_restaurant_info(restaurant_id, name, email, phonenumber, streetadress, zip, city):

    sql = "UPDATE restaurants SET name=:name, email=:email, phonenumber=:phonenumber, streetname=:streetadress, zip=:zip, city=:city WHERE id=:restaurant_id AND is_hidden = false"
    db.session.execute(sql,{"restaurant_id":restaurant_id, "name":name, "email":email, "phonenumber":phonenumber, "streetadress":streetadress, "zip":zip, "city":city})
    db.session.commit()

def set_restaurant_hidden(restaurant_id, owner_id):
    sql = "UPDATE restaurants SET is_hidden= true WHERE id=:restaurant_id AND owner_id=:owner_id"
    db.session.execute(sql,{"restaurant_id":restaurant_id, "owner_id":owner_id})
    db.session.commit()

def set_feedback_resolved(feedback_id):
    sql = "UPDATE feedback SET waiting_action= false WHERE id=:feedback_id"
    db.session.execute(sql,{"feedback_id":feedback_id})
    db.session.commit()

def set_feedback_needs_action(feedback_id):
    sql = "UPDATE feedback SET waiting_action= true WHERE id=:feedback_id"
    db.session.execute(sql,{"feedback_id":feedback_id})
    db.session.commit()

def update_password_customer(id, hashed_password):

    sql = "UPDATE customers SET password=:hashed_password WHERE id=:id"
    db.session.execute(sql,{"id":id, "hashed_password":hashed_password})
    db.session.commit()

def update_password_company(id, hashed_password):

    sql = "UPDATE companys SET password=:hashed_password WHERE id=:id"
    db.session.execute(sql,{"id":id, "hashed_password":hashed_password})
    db.session.commit()

def make_admin(email):
    sql = "UPDATE customers SET is_admin=true WHERE email=:email"
    db.session.execute(sql,{"email":email})
    db.session.commit()

def remove_admin(email):
    sql = "UPDATE customers SET is_admin=false WHERE email=:email"
    db.session.execute(sql,{"email":email})
    db.session.commit()

def enable_customer(email):
    sql = "UPDATE customers SET is_hidden=false WHERE email=:email"
    db.session.execute(sql,{"email":email})
    db.session.commit()

def disable_customer(email):
    sql = "UPDATE customers SET is_hidden=true WHERE email=:email"
    db.session.execute(sql,{"email":email})
    db.session.commit()

def enable_company(email):
    sql = "UPDATE companys SET is_hidden=false WHERE email=:email"
    db.session.execute(sql,{"email":email})
    db.session.commit()

def disable_company(email):
    sql = "UPDATE companys SET is_hidden=true WHERE email=:email"
    db.session.execute(sql,{"email":email})
    db.session.commit()

def recover_review(id):
    sql = "UPDATE reviews SET is_hidden=false WHERE id=:id"
    db.session.execute(sql,{"id":id})
    db.session.commit()

def delete_review(id):
    sql = "UPDATE reviews SET is_hidden=true WHERE id=:id"
    db.session.execute(sql,{"id":id})
    db.session.commit()