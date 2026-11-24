-- Overall delivery KPIs
SELECT
    COUNT(*) AS total_orders,
    ROUND(AVG(CASE WHEN delivery_status = 'On Time' THEN 1.0 ELSE 0.0 END) * 100, 2) AS on_time_rate_pct,
    ROUND(AVG(actual_delivery_days), 2) AS avg_delivery_days,
    ROUND(AVG(delivery_cost_eur), 2) AS avg_delivery_cost_eur
FROM delivery_orders;

-- Carrier performance
SELECT
    carrier,
    COUNT(*) AS total_orders,
    ROUND(AVG(CASE WHEN delivery_status = 'On Time' THEN 1.0 ELSE 0.0 END) * 100, 2) AS on_time_rate_pct,
    ROUND(AVG(actual_delivery_days), 2) AS avg_delivery_days,
    ROUND(AVG(delivery_cost_eur), 2) AS avg_delivery_cost_eur
FROM delivery_orders
GROUP BY carrier
ORDER BY on_time_rate_pct DESC;

-- Rural versus urban delivery performance
SELECT
    delivery_type,
    COUNT(*) AS total_orders,
    ROUND(AVG(CASE WHEN delivery_status = 'On Time' THEN 1.0 ELSE 0.0 END) * 100, 2) AS on_time_rate_pct,
    ROUND(AVG(actual_delivery_days), 2) AS avg_delivery_days
FROM delivery_orders
GROUP BY delivery_type;

-- Monthly delivery performance
SELECT
    strftime('%Y-%m', order_date) AS order_month,
    COUNT(*) AS total_orders,
    ROUND(AVG(CASE WHEN delivery_status = 'On Time' THEN 1.0 ELSE 0.0 END) * 100, 2) AS on_time_rate_pct
FROM delivery_orders
GROUP BY order_month
ORDER BY order_month;
