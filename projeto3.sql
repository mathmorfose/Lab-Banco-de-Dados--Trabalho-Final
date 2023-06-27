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

-- Criação da tabela para armazenar os logs
DROP TABLE IF EXISTS LogTable CASCADE;
CREATE TABLE LogTable (
  userid INTEGER NOT NULL,
  login_date DATE,
  login_time TIME,
  CONSTRAINT fk_userid FOREIGN KEY (userid) REFERENCES USERS (UserId)
);


-- Preenche a tabela Users com pilotos já existentes na base de dados
INSERT INTO users (login, password, tipo, idoriginal)
SELECT CONCAT(driverref, '_d'), MD5(driverref), 'Piloto', driverid
FROM driver;

-- Preenche a tabela Users com escuderias já existentes na base de dados
INSERT INTO users (login, password, tipo, idoriginal)
SELECT CONCAT(constructorref, '_c'), MD5(constructorref), 'Escuderia', constructorid
FROM constructors;

-- Altera a tabela Driver para o ID ser sequencial e adicionado automaticamente ao fazer uma nova inserção
CREATE SEQUENCE my_serial AS integer START 860 OWNED BY DRIVER.DriverId;
ALTER TABLE driver ALTER COLUMN DriverId SET DEFAULT nextval('my_serial');

-- Altera a tabela Constructor para o ID ser sequencial e adicionado automaticamente ao fazer uma nova inserção
CREATE SEQUENCE my_serial2 AS integer START 216 OWNED BY CONSTRUCTORS.ConstructorId;
ALTER TABLE constructors ALTER COLUMN ConstructorId SET DEFAULT nextval('my_serial2');



