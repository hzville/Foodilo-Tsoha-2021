
##Customer table:

CREATE TABLE customers (id SERIAL PRIMARY KEY, email TEXT UNIQUE NOT NULL, type TEXT NOT NULL DEFAULT 'customer', firstname TEXT NOT NULL, lastname TEXT NOT NULL, phonenumber BIGINT UNIQUE NOT NULL, streetname TEXT NOT NULL, zip INT NOT NULL, country TEXT NOT NULL DEFAULT 'FINLAND', singupdate DATE DEFAULT NOW(), password TEXT NOT NULL); 


_______________________________________________________________________________________________________________________________________

##Company table:

CREATE TABLE companys (id SERIAL PRIMARY KEY, email TEXT UNIQUE NOT NULL, type TEXT NOT NULL DEFAULT 'company', name TEXT NOT NULL, businessid TEXT NOT NULL, contactname TEXT NOT NULL, contactnumber BIGINT NOT NULL, streetname TEXT NOT NULL, zip INT NOT NULL, country TEXT NOT NULL DEFAULT 'FINLAND', singupdate DATE DEFAULT NOW(), password TEXT NOT NULL);


_______________________________________________________________________________________________________________________________________

##Restaurant table:
CREATE TABLE restaurants (id SERIAL PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL, phonenumber BIGINT NOT NULL, streetname TEXT NOT NULL, zip INT NOT NULL, country TEXT NOT NULL DEFAULT 'FINLAND', dateadded DATE NOT NULL DEFAULT NOW(), ownerid BIGINT NOT NULL, ishidden INT NOT NULL DEFAULT 0); 

_______________________________________________________________________________________________________________________________________

##Reviews table:

CREATE TABLE reviews (id SERIAL PRIMARY KEY, restaurantid BIGINT NOT NULL, reviewerid BIGINT NOT NULL, score INT NOT NULL, commentary TEXT NOT NULL, datemade DATE NOT NULL DEFAULT NOW());
