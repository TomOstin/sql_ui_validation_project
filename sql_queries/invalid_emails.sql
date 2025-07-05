-- Находит клиентов с пустыми e-mail
SELECT id, name, email, country
FROM customers
WHERE email IS NULL OR TRIM(email) = '';
