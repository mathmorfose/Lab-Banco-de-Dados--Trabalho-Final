import psycopg2
import credenciais as cd
# Conectar ao banco de dados


conn = psycopg2.connect(
    host="localhost",
    database= cd.DATABASE_NAME,
    user= cd.USER_NAME,
    password= cd.PASSWORD
)


# Criar um cursor
#cursor = conn.cursor()

class BANCO_DADOS():

    def select(query):
        with conn.cursor() as cursor:
            try:
                cursor.execute(query)
            except (Exception, psycopg2.Error) as error:
                print(f"Deu erro no select: {error}")
            return cursor.fetchall()
    
    def insert_construct(constructor_ref, name, nationality, url):
        with conn.cursor() as cursor:
            try:
                sql = "INSERT INTO Constructors (ConstructorRef, Name, Nationality, URL) VALUES (%s, %s, %s, %s)"
                values = (constructor_ref, name, nationality, url)
                cursor.execute(sql, values)

                # Confirmar a transação
                conn.commit()

                print("Sucesso no cadastro de Construtor!")
                return True
            except (Exception, psycopg2.Error) as error:
                print("\nErro ao inserir registro na tabela Construct:", error)
                conn.rollback()
                return False

    def insert_driver(driver_ref, number, code, forename, surname, date_of_birth, nationality):
        with conn.cursor() as cursor:
            try:

                sql = "INSERT INTO Driver (driverRef, number, code, forename, surname, dob, nationality) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (driver_ref, number, code, forename,
                        surname, date_of_birth, nationality)
                
                cursor.execute(sql, values)
                
                # Confirmar a transação
                conn.commit()
                
                print("Sucesso no cadastro de Piloto!")

                return True
            except (Exception, psycopg2.Error) as error:
                print("\nErro ao inserir registro na tabela Driver:", error)
                conn.rollback()
                return False

    def insert_log_table(user, login_date, login_time):
        with conn.cursor() as cursor:
            try:
                sql = f"INSERT INTO LogTable (userid, login_date, login_time) VALUES ('{user}', {login_date}, {login_time})"
                print(sql)
                cursor.execute(sql)
                
                # Confirmar a transação
                conn.commit()
                
                print("Sucesso no cadastro de Piloto!")

                return True
            except (Exception, psycopg2.Error) as error:
                conn.rollback()
                print("\nErro ao inserir registro na tabela LogTable:", error)
                return False

    def consultar_pilotos_por_forename(forename, id_escuderia_logada):
        with conn.cursor() as cursor:
            try:

                # Consultar pilotos com o mesmo Forename que já correram pela escuderia logada
                sql = "SELECT DISTINCT Forename, Surname, dob, Nationality FROM Driver " \
                    "INNER JOIN Results ON Driver.DriverId = Results.DriverId " \
                    "WHERE Forename = %s AND ConstructorId = %s"
                values = (forename, id_escuderia_logada)

                #conn.begin()

                cursor.execute(sql, values)

                # Verificar se existem resultados
                if cursor.rowcount > 0:
                    print("\nPilotos encontrados:")
                    for row in cursor:
                        forename, surname, date_of_birth, nationality = row
                        print("Nome completo:", forename, surname)
                        print("Data de Nascimento(AAAA/MM/DD):", date_of_birth)
                        print("Nacionalidade:", nationality)
                        print("----------------------")
                else:
                    print(
                        "Nenhum piloto encontrado com esse Forename que tenha corrido pela escuderia logada.")


            except (Exception, psycopg2.Error) as error:
                print("Erro durante a consulta de pilotos:", error)
                
# Fechar o cursor e a conexão com o banco de dados
#cur.close()
#conn.close()
