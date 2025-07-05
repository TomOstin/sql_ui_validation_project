-- Ищет заказы, в которых сумма позиций не совпадает с total_amount
SELECT
    o.id AS order_id,
    o.total_amount AS total_from_orders,
    ROUND(SUM(oi.quantity * oi.price), 2) AS total_from_items,
    ABS(o.total_amount - ROUND(SUM(oi.quantity * oi.price), 2)) AS delta
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id
HAVING delta > 0.01;
