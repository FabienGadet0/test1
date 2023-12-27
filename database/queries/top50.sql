-- TOP 50 products sold(called description in the database) per day per country
CREATE VIEW top_50_daily_revenue_per_country AS
SELECT
  description,
  country,
  DATE(invoice_date) AS day,
  SUM(quantity * unit_price) AS total_revenue
FROM
  raw_parsed_products
GROUP BY
  description,
  country,
  DATE(invoice_date)
ORDER BY
  total_revenue DESC
LIMIT 50;

