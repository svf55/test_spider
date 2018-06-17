CREATE TABLE selling (
    id SERIAL PRIMARY KEY,
    collection_ts TIMESTAMP NOT NULL DEFAULT NOW(),
    position INTEGER NOT NULL,
    seller_name VARCHAR(255) NOT NULL,
    payment_method VARCHAR(255) NOT NULL,
    payment_bank VARCHAR(255) NULL,
    price DECIMAL NOT NULL,
    limit_from DECIMAL NOT NULL,
    limit_to DECIMAL NOT NULL,
    currency VARCHAR(3) NOT NULL,
    email_confirmed_date DATE NULL,
    phone_confirmed_date DATE NULL,
    partners_confirmed INTEGER DEFAULT NULL
)
