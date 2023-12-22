-- CREATE DATABASE production;
CREATE SCHEMA IF NOT EXISTS landing;

CREATE TABLE IF NOT EXISTS landing.raw_products (
    id SERIAL PRIMARY KEY,
    data JSONB
);
