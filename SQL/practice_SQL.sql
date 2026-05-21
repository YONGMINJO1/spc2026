-- 1. non_usa_customers.sql: 미국에 거주하지 않는 고객(전체 이름, 고객 ID 및 국가)을 표시하는 쿼리를 제공합니다.
SELECT FirstName ||' '|| LastName , CustomerId, Country
FROM customers 
WHERE Country != 'USA';

-- 2. brazil_customers.sql: 브라질 고객만 표시하는 쿼리를 제공합니다.
SELECT FirstName ||' '|| LastName , CustomerId, Country 
FROM customers 
WHERE Country = 'Brazil';

-- 3. brazil_customers_invoices.sql: 브라질 고객의 송장을 보여주는 쿼리를 제공합니다. 결과 테이블에는 고객의 전체 이름, 송장 ID, 송장 날짜 및 청구 국가가 표시되어야 합니다.
SELECT c.FirstName ||' '|| c.LastName, i.InvoiceId, i.InvoiceDate, i.BillingCountry
FROM customers c
JOIN invoices i on c.CustomerId = i.CustomerId
WHERE c.Country = 'Brazil';

-- 4. sales_agents.sql: 판매 대리인인 직원만 표시하는 쿼리를 제공하십시오.
SELECT  * FROM employees WHERE Title = 'Sales Support Agent';

-- 5. unique_invoice_countries.sql: 송장 테이블에서 청구 국가의 고유(unique)/고유(distinct) 목록을 표시하는 쿼리를 제공합니다.
SELECT DISTINCT BillingCountry FROM invoices;

-- 6. sales_agent_invoices.sql: 각 판매 에이전트와 연결된 송장을 표시하는 쿼리를 제공합니다. 결과 테이블에는 영업 에이전트의 전체 이름이 포함되어야 합니다.
SELECT e.FirstName ||' '|| e.LastName, i. InvoiceId
FROM employees e
JOIN customers c on e.EmployeeId = c.SupportRepId
JOIN Invoices i on c.customerId = i.CustomerId
WHERE e.Title = 'Sales Support Agent'; 

-- 7. invoice_totals.sql: 모든 송장 및 고객에 대한 송장 합계, 고객 이름, 국가 및 판매 대리점 이름을 표시하는 쿼리를 제공합니다.
SELECT c.FirstName ||' '|| c.LastName, c.Country, i.Total, e.FirstName ||' '|| e.LastName 
FROM invoices i 
JOIN customers c ON i.CustomerId = c.CustomerId 
JOIN employees e ON c.SupportRepId = e.EmployeeId 
WHERE e.Title = 'Sales Support Agent';

-- 8. total_invoices_{year}.sql: 2009년과 2011년에 몇 개의 인보이스가 있었습니까?
SELECT COUNT(*)
FROM invoices
WHERE strftime('%Y', InvoiceDate) = '2009'
OR strftime('%Y', InvoiceDate) = '2011';

-- 9. total_sales_{year}.sql: 각 연도의 총 매출은 얼마입니까?
SELECT strftime('%Y', InvoiceDate), SUM(Total)
FROM invoices
GROUP BY strftime('%Y', InvoiceDate);

-- 10. invoice_37_line_item_count.sql: InvoiceLine 테이블을 보고 Invoice ID 37에 대한 라인 항목 수를 계산하는 쿼리를 제공합니다.
SELECT COUNT(*) FROM invoice_items
WHERE InvoiceId = 37;

-- 11. line_items_per_invoice.sql: InvoiceLine 테이블을 보고 각 Invoice에 대한 라인 항목 수를 계산하는 쿼리를 제공합니다. 힌트: 그룹화 기준
SELECT InvoiceId, COUNT(*)
FROM invoice_items
GROUP BY InvoiceId;

-- 12. line_item_track.sql: 각 송장 라인 항목에 구매한 트랙 이름을 포함하는 쿼리를 제공합니다.
SELECT i.InvoiceLineId, i.InvoiceId, t.Name
FROM invoice_items i
JOIN tracks t ON i.TrackId = t.TrackId;

-- 13. line_item_track_artist.sql: 구매한 트랙 이름과 아티스트 이름을 포함하는 쿼리를 각 송장 라인 항목과 함께 제공합니다.
SELECT ii.InvoiceLineId, ii.InvoiceId, t.Name, ar.Name
FROM invoice_items ii
JOIN tracks t ON ii.TrackId = t.TrackId
JOIN albums al ON t.AlbumId = al.AlbumId

-- 14. country_invoices.sql: 국가별 송장 수를 표시하는 쿼리를 제공합니다. 힌트: 그룹화 기준
SELECT BillingCountry, COUNT(*)
FROM invoices
GROUP BY BillingCountry;

-- 15. playlists_track_count.sql: 각 재생 목록의 총 트랙 수를 표시하는 쿼리를 제공합니다. 재생 목록 이름은 결과 테이블에 포함되어야 합니다.
SELECT p.Name, COUNT(*)
FROM playlists p
JOIN playlist_track pt ON p.PlaylistId = pt.PlaylistId
GROUP BY p.PlaylistId;

-- 16. Tracks_no_id.sql: 모든 트랙을 표시하지만 ID는 표시하지 않는 쿼리를 제공합니다. 결과에는 앨범 이름, 미디어 유형 및 장르가 포함되어야 합니다.
SELECT t.Name, al.Title, mt.Name, g.Name
FROM tracks t
JOIN albums al      ON t.AlbumId = al.AlbumId
JOIN media_types mt ON t.MediaTypeId = mt.MediaTypeId
JOIN genres g       ON t.GenreId = g.GenreId;

-- 17. invoices_line_item_count.sql: 모든 송장을 표시하지만 송장 라인 항목의 수를 포함하는 쿼리를 제공합니다.
SELECT i.InvoiceId, i.CustomerId, i.InvoiceDate, i.Total, COUNT(ii.InvoiceLineId) 
FROM invoices i
JOIN invoice_items ii ON i.InvoiceId = ii.InvoiceId
GROUP BY i.InvoiceId;

-- 18. sales_agent_total_sales.sql: 판매 대리점별 총 매출을 조회하는 쿼리를 제공한다.
SELECT e.FirstName ||' '|| e.LastName, SUM(i.Total)
FROM employees e
JOIN customers c ON e.EmployeeId = c.SupportRepId
JOIN invoices i  ON c.CustomerId = i.CustomerId
WHERE e.Title = 'Sales Support Agent'
GROUP BY e.EmployeeId;

-- 19. top_2009_agent.sql: 2009년 가장 많은 매출을 올린 판매원은?
--     힌트: 하위 쿼리에서 MAX 함수를 사용하십시오. 

-- 20. top_agent.sql: 전체 판매 실적이 가장 많은 판매 대리점은?

-- 21. sales_agent_customer_count.sql: 각 판매 대리점에 할당된 고객 수를 보여주는 쿼리를 제공한다.

-- 22. sales_per_country.sql: 국가별 총 매출을 보여주는 쿼리를 제공한다.

-- 23. top_country.sql: 고객이 가장 많이 지출한 국가는 어디입니까?

-- 24. top_2013_track.sql: 2013년 가장 많이 구매한 트랙을 보여주는 쿼리를 제공합니다.

-- 25. top_5_tracks.sql: 가장 많이 구매한 상위 5곡을 보여주는 쿼리를 제공합니다.

-- 26. top_3_artists.sql: 가장 많이 팔린 3명의 아티스트를 보여주는 쿼리를 제공합니다.

-- 27. top_media_type.sql: 가장 많이 구매한 Media Type을 보여주는 쿼리를 제공한다.