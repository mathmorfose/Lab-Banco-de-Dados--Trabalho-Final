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
WHERE isocountry = 'BR' AND type IN ('medium_airport', 'large_airport');
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

-- relatórios escuderia

-- 3
DROP INDEX IF EXISTS IdxResultsConstructors;
CREATE INDEX IdxResultsConstructors 
ON results 
USING BTREE(constructorID)
INCLUDE (driverID, position)
;

CREATE OR REPLACE FUNCTION get_numero_vitorias_pilotos_da_escuderia(escuderia_id INTEGER)
RETURNS TABLE (
    nome_completo TEXT,
    quantidade BIGINT
)
AS $$
BEGIN
  RETURN QUERY
    SELECT 
        D.forename || ' ' || D.surname AS nome_completo,
        COUNT(CASE WHEN R.position = 1 THEN 1 ELSE NULL END) AS quantidade
    FROM results R
        JOIN driver D ON R.driverID = D.driverID AND R.constructorID = escuderia_id
    GROUP BY nome_completo
    ORDER BY quantidade DESC
    ;
END;
$$ LANGUAGE plpgsql;

-- 4
CREATE OR REPLACE FUNCTION get_contagem_status_da_escuderia(escuderia_id INTEGER)
RETURNS TABLE (
    status TEXT,
    quantidade_resultados BIGINT
)
AS $$
BEGIN
  RETURN QUERY
    SELECT s.status, COUNT(r.statusid) AS quantidade_resultados 
    FROM status s 
    JOIN results r ON s.statusid = r.statusid AND r.constructorID = escuderia_id
    GROUP BY s.status 
    ORDER BY quantidade_resultados DESC
    ;
END;
$$ LANGUAGE plpgsql;

-- relatórios piloto

-- 5
DROP INDEX IF EXISTS IdxResultsWinners;
CREATE INDEX IdxResultsWinners
ON results 
USING BTREE(driverID)
INCLUDE(raceID)
WHERE position = 1
;

CREATE OR REPLACE FUNCTION get_all_vitorias_piloto(piloto_id INTEGER)
RETURNS TABLE (
    name TEXT,
    year INTEGER,
	vitorias BIGINT
)
AS $$
BEGIN
  RETURN QUERY
    SELECT RA.name, RA.year, COUNT(*) AS vitorias
	FROM results RE
		JOIN races RA ON RA.raceID = RE.raceID
	WHERE 
		RE.driverID = piloto_id AND position = 1
	GROUP BY ROLLUP(RA.year, RA.name)
	ORDER BY RA.year NULLS FIRST, RA.name NULLS FIRST
	;
END;
$$ LANGUAGE plpgsql;

-- 6
CREATE OR REPLACE FUNCTION get_contagem_status_do_piloto(piloto_id INTEGER)
RETURNS TABLE (
    status TEXT,
    quantidade_resultados BIGINT
)
AS $$
BEGIN
  RETURN QUERY
    SELECT s.status, COUNT(r.statusid) AS quantidade_resultados 
    FROM status s 
    JOIN results r ON s.statusid = r.statusid AND r.driverID = piloto_id
    GROUP BY s.status 
    ORDER BY quantidade_resultados DESC
    ;
END;
$$ LANGUAGE plpgsql;
