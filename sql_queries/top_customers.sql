-- Топ-5 клиентов по общей сумме заказов
SELECT
    c.id AS customer_id,
    c.name,
    c.country,
    COUNT(o.id) AS order_count,
    ROUND(SUM(o.total_amount), 2) AS total_spent
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id
ORDER BY total_spent DESC
LIMIT 5;
