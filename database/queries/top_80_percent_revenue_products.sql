CREATE VIEW public.top_80_percent_revenue_products AS
WITH ProductRevenue AS (
  SELECT
    stock_code,
    description,
    quantity,
    unit_price,
    quantity * unit_price AS revenue,
    SUM(quantity * unit_price) OVER (ORDER BY quantity * unit_price DESC) AS cumulative_revenue,
    SUM(quantity * unit_price) OVER () AS total_revenue
  FROM
    landing.raw_parsed_products
)
SELECT
  stock_code,
  description,
  quantity,
  unit_price,
  revenue,
  ROUND((cumulative_revenue / total_revenue) * 100, 2) AS cumulative_revenue_percent,
  ROUND((revenue / total_revenue) * 100, 2) AS percentage_of_total_revenue
FROM
  ProductRevenue
WHERE
  (cumulative_revenue / total_revenue) * 100 <= 80;
