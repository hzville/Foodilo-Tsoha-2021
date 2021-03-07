

CREATE TABLE customers (id SERIAL PRIMARY KEY, email TEXT UNIQUE NOT NULL, firstname TEXT NOT NULL, lastname TEXT NOT NULL, singupdate DATE DEFAULT NOW(), password TEXT NOT NULL, is_hidden BOOLEAN NOT NULL DEFAULT FALSE, is_admin BOOLEAN NOT NULL DEFAULT FALSE); 



CREATE TABLE companys (id SERIAL PRIMARY KEY, email TEXT UNIQUE NOT NULL, name TEXT NOT NULL, business_id TEXT NOT NULL, contactname TEXT NOT NULL, contactnumber TEXT NOT NULL, streetname TEXT NOT NULL, zip TEXT NOT NULL, country TEXT NOT NULL DEFAULT 'FINLAND', singupdate DATE DEFAULT NOW(), password TEXT NOT NULL, is_hidden BOOLEAN NOT NULL DEFAULT FALSE);




CREATE TABLE restaurants (id SERIAL PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL, phonenumber TEXT NOT NULL, streetname TEXT NOT NULL, zip TEXT NOT NULL, city TEXT NOT NULL, country TEXT NOT NULL DEFAULT 'FINLAND', dateadded DATE NOT NULL DEFAULT NOW(), owner_id BIGINT REFERENCES companys(id) NOT NULL, is_hidden boolean NOT NULL DEFAULT false); 



CREATE TABLE reviews (id SERIAL PRIMARY KEY, restaurant_id BIGINT REFERENCES restaurants(id) NOT NULL, restaurant_name TEXT NOT NULL, reviewer_firstname TEXT NOT NULL, reviewer_lastname TEXT NOT NULL, reviewer_id BIGINT REFERENCES customers(id) NOT NULL, score INT NOT NULL, commentary TEXT NOT NULL, datemade DATE NOT NULL DEFAULT NOW(), is_hidden BOOLEAN NOT NULL DEFAULT FALSE);



CREATE TABLE postnumber_mapping (id SERIAL PRIMARY KEY, postnumber TEXT UNIQUE NOT NULL, city TEXT NOT NULL);


CREATE TABLE feedback (id SERIAL PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL, feedback TEXT NOT NULL, waiting_action BOOLEAN NOT NULL DEFAULT TRUE, date DATE NOT NULL DEFAULT NOW());





