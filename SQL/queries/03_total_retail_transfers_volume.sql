-- 3. Total Retail Transfers Volume
SELECT ROUND(SUM(retail_transfers), 2) AS total_retail_transfers_volume
FROM sales;
