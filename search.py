from db import db 

def get_restaurants(query):
    sql = "SELECT id, name, streetname, zip, city, phonenumber FROM restaurants WHERE is_hidden=false AND name ILIKE :query OR city ILIKE :query"
    result = db.session.execute(sql,{"query":"%"+query+"%"})
    result_to_return = result.fetchall()

    return result_to_return