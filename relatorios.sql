-- relatórios admin

-- 1
SELECT s.status, COUNT(r.statusid) AS quantidade_resultados 
FROM status s 
LEFT JOIN results r ON s.statusid = r.statusid 
GROUP BY s.status 
ORDER BY quantidade_resultados DESC
;

-- 2
CREATE EXTENSION IF NOT EXISTS Cube;
CREATE EXTENSION IF NOT EXISTS EarthDistance;

DROP INDEX IF EXISTS IdxNameCities;
CREATE INDEX IdxNameCities
ON geocities15k 
USING HASH(name)
;

DROP INDEX IF EXISTS IdxBrazilianMediumLargeAirports;
CREATE INDEX IdxBrazilianMediumLargeAirports
ON airports 
USING BTREE(type)
WHERE isocountry = 'BR'
;

CREATE OR REPLACE FUNCTION get_aeroportos_proximos(nome_cidade TEXT)
RETURNS TABLE (
    cidade TEXT,
    iatacode CHAR(3),
    aeroporto TEXT,
    cidade_aeroporto TEXT,
    distancia NUMERIC,
    type CHAR(15)
)
AS $$
BEGIN
  RETURN QUERY
    SELECT 
        C.name cidade, A.iatacode, A.name aeroporto, 
        A.city cidade_aeroporto,
        round((Earth_Distance(
            LL_to_Earth(A.latdeg, A.longdeg), 
            LL_to_Earth(C.lat, C.long)
        )/1000)::numeric, 2) distancia,
        A.type 
    FROM airports A
    JOIN geocities15k C ON Earth_Distance(
        LL_to_Earth(
            A.latdeg, 
            A.longdeg), 
        LL_to_Earth(
            C.lat, 
            C.long)
        ) <= 100000
    WHERE 
        A.isocountry = 'BR' AND
        A.type IN ('medium_airport', 'large_airport') AND
        C.name = nome_cidade
    ORDER BY distancia;
END;
$$ LANGUAGE plpgsql;
