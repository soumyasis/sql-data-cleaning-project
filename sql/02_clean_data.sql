DROP TABLE IF EXISTS clean_customers;

CREATE TABLE clean_customers AS
WITH ranked AS (
    SELECT
        s.*,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY customer_id) AS rn
    FROM stg_customers s
)
SELECT
    TRIM(customer_id) AS customer_id,
    CONCAT(UPPER(LEFT(TRIM(first_name), 1)), LOWER(SUBSTRING(TRIM(first_name), 2))) AS first_name,
    CASE
        WHEN NULLIF(TRIM(middle_name), '') IS NULL THEN NULL
        ELSE CONCAT(UPPER(LEFT(TRIM(middle_name), 1)), LOWER(SUBSTRING(TRIM(middle_name), 2)))
    END AS middle_name,
    CONCAT(UPPER(LEFT(TRIM(last_name), 1)), LOWER(SUBSTRING(TRIM(last_name), 2))) AS last_name,
    CASE
        WHEN LOWER(TRIM(sex)) IN ('m', 'male')   THEN 'Male'
        WHEN LOWER(TRIM(sex)) IN ('f', 'female') THEN 'Female'
        ELSE 'Unknown'
    END AS sex,
    CAST(NULLIF(TRIM(date_of_birth), '') AS DATE) AS date_of_birth,
    LOWER(TRIM(email)) AS email,
    CONCAT(UPPER(LEFT(TRIM(city), 1)), LOWER(SUBSTRING(TRIM(city), 2))) AS city,
    TRIM(segment) AS segment,
    CAST(NULLIF(TRIM(signup_date), '') AS DATE) AS signup_date
FROM ranked
WHERE rn = 1;