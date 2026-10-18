CREATE TABLE `gold_analytics.fact_orders` (
  order_id STRING NOT NULL,
  customer_id STRING NOT NULL,
  order_date DATE NOT NULL,
  total_amount_usd FLOAT64 NOT NULL,
  items_count INT64 NOT NULL,
  status STRING NOT NULL
);
