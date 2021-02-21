

CREATE TABLE customers (id SERIAL PRIMARY KEY, email TEXT UNIQUE NOT NULL, firstname TEXT NOT NULL, lastname TEXT NOT NULL, phonenumber BIGINT UNIQUE NOT NULL, streetname TEXT NOT NULL, zip INT NOT NULL, country TEXT NOT NULL DEFAULT 'FINLAND', singupdate DATE DEFAULT NOW(), password TEXT NOT NULL); 




CREATE TABLE companys (id SERIAL PRIMARY KEY, email TEXT UNIQUE NOT NULL, name TEXT NOT NULL, business_id TEXT NOT NULL, contactname TEXT NOT NULL, contactnumber BIGINT NOT NULL, streetname TEXT NOT NULL, zip INT NOT NULL, country TEXT NOT NULL DEFAULT 'FINLAND', singupdate DATE DEFAULT NOW(), password TEXT NOT NULL);




CREATE TABLE restaurants (id SERIAL PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL, phonenumber TEXT NOT NULL, streetname TEXT NOT NULL, zip TEXT NOT NULL, city TEXT, country TEXT NOT NULL DEFAULT 'FINLAND', dateadded DATE NOT NULL DEFAULT NOW(), owner_id BIGINT NOT NULL, is_hidden boolean NOT NULL DEFAULT false); 



CREATE TABLE reviews (id SERIAL PRIMARY KEY, restaurant_id BIGINT NOT NULL, reviewer_firstname TEXT NOT NULL, reviewer_lastname TEXT NOT NULL, reviewer_id BIGINT NOT NULL, score INT NOT NULL, commentary TEXT NOT NULL, datemade DATE NOT NULL DEFAULT NOW());




CREATE TABLE postnumber_mapping (id SERIAL PRIMARY KEY, postnumber TEXT, city TEXT);



