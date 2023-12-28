--  DATABASE production;
CREATE SCHEMA IF NOT EXISTS landing;

CREATE TABLE IF NOT EXISTS landing.raw_products (
    id SERIAL PRIMARY KEY,
    data JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS landing.raw_parsed_products (
    id SERIAL PRIMARY KEY,
    country VARCHAR(255),
    quantity INTEGER NOT NULL, 
    invoice_no VARCHAR(255), 
    stock_code VARCHAR(255),
    unit_price NUMERIC(10, 2) NOT NULL, 
    customer_id VARCHAR(255),
    description VARCHAR(255) NOT NULL,
    invoice_date TIMESTAMP,

    CONSTRAINT superkey_constraint UNIQUE (invoice_date, description, quantity, invoice_no) -- help avoid duplicates
);
