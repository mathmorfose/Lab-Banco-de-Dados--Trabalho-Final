-- Criando a tabela USERS
DROP TABLE IF EXISTS USERS CASCADE;
CREATE TABLE USERS (
  UserId SERIAL PRIMARY KEY,
  Login VARCHAR(50) UNIQUE NOT NULL,
  Password TEXT NOT NULL,
  Tipo VARCHAR(50) NOT NULL,
  IdOriginal NUMERIC(8) NOT NULL,
  CONSTRAINT CHK_TIPO CHECK (Tipo IN ('Administrador', 'Escuderia', 'Piloto'))
);

DROP TRIGGER IF EXISTS trigger_md5_password ON USERS;
DROP FUNCTION IF EXISTS md5_password();

-- Criação de funções e gatilhos para a inserção automática de pilotos e escuderias na tabela users

-- Gatilho para inserção de pilotos na tabela USERS
CREATE OR REPLACE FUNCTION insert_piloto_user()
  RETURNS TRIGGER AS $$
BEGIN
  -- Inserir na tabela USERS
  INSERT INTO USERS (Login, Password, Tipo, IdOriginal)
  VALUES (NEW.DriverRef || '_d', MD5(NEW.DriverRef), 'Piloto', NEW.DriverId);
  RETURN NEW;
EXCEPTION
  WHEN unique_violation THEN
    RAISE EXCEPTION 'O login informado já está em uso.' USING ERRCODE='23505';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_insert_piloto_user ON DRIVER;
CREATE TRIGGER trigger_insert_piloto_user
  AFTER INSERT ON DRIVER
  FOR EACH ROW
  EXECUTE FUNCTION insert_piloto_user();

-- Gatilho para atualização de pilotos na tabela USERS
CREATE OR REPLACE FUNCTION update_piloto_user()
  RETURNS TRIGGER AS $$
BEGIN
  -- Atualizar na tabela USERS
  UPDATE USERS
  SET Login = NEW.DriverRef || '_d',
      Password = MD5(NEW.DriverRef)
  WHERE IdOriginal = NEW.DriverId AND Tipo = 'Piloto';
  RETURN NEW;
EXCEPTION
  WHEN unique_violation THEN
    RAISE EXCEPTION 'O login informado já está em uso.' USING ERRCODE='23505';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_update_piloto_user ON DRIVER;
CREATE TRIGGER trigger_update_piloto_user
  AFTER UPDATE ON DRIVER
  FOR EACH ROW
  EXECUTE FUNCTION update_piloto_user();

-- Gatilho para remoção de pilotos na tabela USERS
CREATE OR REPLACE FUNCTION delete_piloto_user()
  RETURNS TRIGGER AS $$
BEGIN
  -- Remover da tabela USERS
  DELETE FROM USERS
  WHERE IdOriginal = OLD.DriverId AND Tipo = 'Piloto';
  RETURN OLD;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_delete_piloto_user ON DRIVER;
CREATE TRIGGER trigger_delete_piloto_user
  AFTER DELETE ON DRIVER
  FOR EACH ROW
  EXECUTE FUNCTION delete_piloto_user();

-- Gatilho para inserção de escuderias na tabela USERS
CREATE OR REPLACE FUNCTION insert_escuderia_user()
  RETURNS TRIGGER AS $$
BEGIN
  -- Inserir na tabela USERS
  INSERT INTO USERS (Login, Password, Tipo, IdOriginal)
  VALUES (NEW.ConstructorRef || '_c', MD5(NEW.ConstructorRef), 'Escuderia', NEW.ConstructorId);
  RETURN NEW;
EXCEPTION
  WHEN unique_violation THEN
    RAISE EXCEPTION 'O login informado já está em uso.' USING ERRCODE='23505';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_insert_escuderia_user ON CONSTRUCTORS;
CREATE TRIGGER trigger_insert_escuderia_user
  AFTER INSERT ON CONSTRUCTORS
  FOR EACH ROW
  EXECUTE FUNCTION insert_escuderia_user();

-- Gatilho para atualização de escuderias na tabela USERS
CREATE OR REPLACE FUNCTION update_escuderia_user()
  RETURNS TRIGGER AS $$
BEGIN
  -- Atualizar na tabela USERS
  UPDATE USERS
  SET Login = NEW.ConstructorRef || '_c',
      Password = MD5(NEW.ConstructorRef)
  WHERE IdOriginal = NEW.ConstructorId AND Tipo = 'Escuderia';
  RETURN NEW;
EXCEPTION
  WHEN unique_violation THEN
    RAISE EXCEPTION 'O login informado já está em uso.' USING ERRCODE='23505';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_update_escuderia_user ON CONSTRUCTORS;
CREATE TRIGGER trigger_update_escuderia_user
  AFTER UPDATE ON CONSTRUCTORS
  FOR EACH ROW
  EXECUTE FUNCTION update_escuderia_user();

-- Gatilho para remoção de escuderias na tabela USERS
CREATE OR REPLACE FUNCTION delete_escuderia_user()
  RETURNS TRIGGER AS $$
BEGIN
  -- Remover da tabela USERS
  DELETE FROM USERS
  WHERE IdOriginal = OLD.ConstructorId AND Tipo = 'Escuderia';
  RETURN OLD;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_delete_escuderia_user ON CONSTRUCTORS;
CREATE TRIGGER trigger_delete_escuderia_user
  AFTER DELETE ON CONSTRUCTORS
  FOR EACH ROW
  EXECUTE FUNCTION delete_escuderia_user();

-- Criação da tabela para armazenar os logs
DROP TABLE IF EXISTS LogTable CASCADE;
CREATE TABLE LogTable (
  userid INTEGER NOT NULL,
  login_date DATE,
  login_time TIME,
  CONSTRAINT fk_userid FOREIGN KEY (userid) REFERENCES USERS (UserId)
);

-- Inserindo admin na tabela Users
INSERT INTO users (login, password, tipo, idoriginal)
VALUES ('admin', MD5('admin'), 'Administrador', 0);

-- Preenche a tabela Users com pilotos já existentes na base de dados
INSERT INTO users (login, password, tipo, idoriginal)
SELECT CONCAT(driverref, '_d'), MD5(driverref), 'Piloto', driverid
FROM driver;

-- Preenche a tabela Users com escuderias já existentes na base de dados
INSERT INTO users (login, password, tipo, idoriginal)
SELECT CONCAT(constructorref, '_c'), MD5(constructorref), 'Escuderia', constructorid
FROM constructors;

-- Altera a tabela Driver para o ID ser sequencial e adicionado automaticamente ao fazer uma nova inserção
DROP SEQUENCE IF EXISTS my_serial CASCADE;
CREATE SEQUENCE my_serial AS integer START 860 OWNED BY DRIVER.DriverId;
ALTER TABLE driver ALTER COLUMN DriverId SET DEFAULT nextval('my_serial');

-- Altera a tabela Constructor para o ID ser sequencial e adicionado automaticamente ao fazer uma nova inserção
DROP SEQUENCE IF EXISTS my_serial2 CASCADE;
CREATE SEQUENCE my_serial2 AS integer START 216 OWNED BY CONSTRUCTORS.ConstructorId;
ALTER TABLE constructors ALTER COLUMN ConstructorId SET DEFAULT nextval('my_serial2');

-- Overview Escuderia
-- Função para obter a quantidade de vitórias da escuderia
CREATE OR REPLACE FUNCTION get_escuderia_vitorias(escuderia_id NUMERIC)
  RETURNS INTEGER AS $$
DECLARE
  total_vitorias INTEGER;
BEGIN
  SELECT COUNT(*) INTO total_vitorias
  FROM RESULTS
  WHERE ConstructorId = escuderia_id AND position = 1;

  RETURN total_vitorias;
END;
$$ LANGUAGE plpgsql;

-- Função para obter a quantidade de pilotos diferentes que já correram pela escuderia
CREATE OR REPLACE FUNCTION get_quantidade_pilotos(escuderia_id NUMERIC)
  RETURNS INTEGER AS $$
DECLARE
  total_pilotos INTEGER;
BEGIN
  SELECT COUNT(DISTINCT DriverId) INTO total_pilotos
  FROM RESULTS
  WHERE ConstructorId = escuderia_id;

  RETURN total_pilotos;
END;
$$ LANGUAGE plpgsql;

-- Função para obter o primeiro e último ano de dados da escuderia
CREATE OR REPLACE FUNCTION get_primeiro_ultimo_ano_escuderia(escuderia_id NUMERIC, OUT primeiro_ano INTEGER, OUT ultimo_ano INTEGER)
  RETURNS RECORD AS $$
BEGIN
  SELECT MIN(R.Year), MAX(R.Year)
  INTO primeiro_ano, ultimo_ano
  FROM Results RS
  JOIN Races R ON RS.RaceId = R.RaceId
  WHERE RS.ConstructorId = escuderia_id;

  RETURN;
END;
$$ LANGUAGE plpgsql;

-- Overview Piloto
-- Função para obter o primeiro e último ano de dados da escuderia
CREATE OR REPLACE FUNCTION get_quantidade_vitorias_piloto(piloto_id NUMERIC)
  RETURNS INTEGER AS $$
DECLARE
  quantidade_vitorias INTEGER;
BEGIN
  SELECT COUNT(*) INTO quantidade_vitorias
  FROM RESULTS
  WHERE DriverId = piloto_id
    AND PositionText = '1';

  RETURN quantidade_vitorias;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_primeiro_ultimo_ano_piloto(piloto_id NUMERIC, OUT primeiro_ano INTEGER, OUT ultimo_ano INTEGER)
  RETURNS RECORD AS $$
BEGIN
  SELECT MIN(R.Year), MAX(R.Year)
  INTO primeiro_ano, ultimo_ano
  FROM Results RS
  JOIN Races R ON RS.RaceId = R.RaceId
  WHERE RS.DriverId = piloto_id;

  RETURN;
END;
$$ LANGUAGE plpgsql;

-- Relatórios Admin
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

-- Relatórios Escuderia
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

-- Relatórios Piloto

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
