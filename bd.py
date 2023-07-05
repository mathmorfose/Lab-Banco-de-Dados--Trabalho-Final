import psycopg2
import psycopg2.extras
import credenciais as cd
from utils import formatar_query 

CONNECTION_PARAMS = {
    'host': "localhost",
    'database': cd.DATABASE_NAME,
    'user': cd.USER_NAME,
    'password': cd.PASSWORD,
}

class BANCO_DADOS():

    def select(query):
        selected_rows = None

        # inicia conexão
        conn = psycopg2.connect(**CONNECTION_PARAMS)
        
        # inicia e commita automaticamente transaction
        with conn:
            # cria e fecha automaticamente cursor
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                try:
                    cursor.execute(query)
                    selected_rows = cursor.fetchall()
                except (Exception, psycopg2.Error) as error:
                    print(f"\nErro na execução do select: {error}")
        conn.close()
        return selected_rows
    
    def insert_construct(constructor_ref, name, nationality, url):
        result = None

        conn = psycopg2.connect(**CONNECTION_PARAMS)
        with conn:
            with conn.cursor() as cursor:
                try:
                    sql = "INSERT INTO Constructors (ConstructorRef, Name, Nationality, URL) VALUES ({},{},{},{})"
                    values = (constructor_ref, name, nationality, url)
                    
                    cursor.execute(
                        formatar_query(sql, values)
                    )
                    result = True
                except (Exception, psycopg2.Error) as error:
                    print("\nErro ao inserir registro na tabela Construct:", error)
                    result = False
        conn.close()
        return result

    def insert_driver(driver_ref, number, code, forename, surname, date_of_birth, nationality):
        result = None

        conn = psycopg2.connect(**CONNECTION_PARAMS)
        with conn:
            with conn.cursor() as cursor:
                try:
                    sql = "INSERT INTO Driver (driverRef, number, code, forename, surname, dob, nationality) VALUES ({},{},{},{},{},{},{})"
                    values = (driver_ref, number, code, forename,
                            surname, date_of_birth, nationality)
                    
                    cursor.execute(
                        formatar_query(sql, values)
                    )
                    result = True
                except (Exception, psycopg2.Error) as error:
                    print("\nErro ao inserir registro na tabela Driver:", error)
                    result = False
        conn.close()
        return result

    def insert_log_table(user):
        result = None

        conn = psycopg2.connect(**CONNECTION_PARAMS)
        with conn:
            with conn.cursor() as cursor:
                try:
                    sql = "INSERT INTO LogTable (userid, login_date, login_time) VALUES ({}, CURRENT_DATE, CURRENT_TIME)"
                    values = (user,)
                    
                    cursor.execute(
                        formatar_query(sql, values)
                    )
                    result = True
                except (Exception, psycopg2.Error) as error:
                    print("\nErro ao inserir registro na tabela LogTable:", error)
                    result = False
        conn.close()
        return result

    def consultar_pilotos_por_forename(forename, id_escuderia_logada):
        conn = psycopg2.connect(**CONNECTION_PARAMS)
        with conn:
            with conn.cursor() as cursor:
                try:
                    # Consultar pilotos com o mesmo Forename que já correram pela escuderia logada
                    sql = "SELECT DISTINCT Forename, Surname, dob, Nationality FROM Driver " \
                        "INNER JOIN Results ON Driver.DriverId = Results.DriverId " \
                        "WHERE Forename = %s AND ConstructorId = %s"
                    values = (forename, id_escuderia_logada)

                    cursor.execute(sql, values)
                    selected_rows = cursor.fetchall()
                except (Exception, psycopg2.Error) as error:
                    print("Erro durante a consulta de pilotos:", error)
        conn.close()

        # Verificar se existem resultados
        if len(selected_rows) > 0:
            print("\nPilotos encontrados:")
            for row in selected_rows:
                forename, surname, date_of_birth, nationality = row
                print("Nome completo:", forename, surname)
                print("Data de Nascimento(AAAA/MM/DD):", date_of_birth)
                print("Nacionalidade:", nationality)
                print("----------------------")
        else:
            print("Nenhum piloto encontrado com esse Forename que tenha corrido pela escuderia logada.")
    
    def overview_escuderia(escuderia_id):
        result = None

        conn = psycopg2.connect(**CONNECTION_PARAMS)
        with conn:
            with conn.cursor() as cursor:
                try:
                    # Nome da função e parâmetro
                    cursor.callproc("get_escuderia_vitorias", (escuderia_id,))
                    quantidade_vitorias = cursor.fetchone()[0]

                    cursor.callproc("get_quantidade_pilotos", (escuderia_id,))
                    total_pilotos = cursor.fetchone()[0]

                    cursor.callproc("get_primeiro_ultimo_ano_escuderia", (escuderia_id,))
                    primeiro_ano, ultimo_ano = cursor.fetchone()
                    
                    result = (quantidade_vitorias, total_pilotos, primeiro_ano, ultimo_ano)
                except (Exception, psycopg2.Error) as error:
                    print("Erro ao executar a função:", error)
        conn.close()
        return result

    def overview_piloto(piloto_id):
        result = None

        conn = psycopg2.connect(**CONNECTION_PARAMS)
        with conn:
            with conn.cursor() as cursor:
                try:
                    cursor.callproc("get_quantidade_vitorias_piloto", (piloto_id,))
                    resultado = cursor.fetchone()[0]

                    cursor.callproc("get_primeiro_ultimo_ano_piloto", (piloto_id,))
                    primeiro_ano, ultimo_ano = cursor.fetchone()
                    result = (resultado, primeiro_ano, ultimo_ano)
                except (Exception, psycopg2.Error) as error:
                    print("Erro:", error)
        conn.close()
        return result

    def get_contagem_resultados_status():
        result = None

        conn = psycopg2.connect(**CONNECTION_PARAMS)
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                try:
                    sql =   "SELECT s.status, COUNT(r.statusid) AS quantidade_resultados \
                            FROM status s \
                            LEFT JOIN results r ON s.statusid = r.statusid \
                            GROUP BY s.status \
                            ORDER BY quantidade_resultados DESC;"
                    cursor.execute(sql)
                    result = cursor.fetchall()
                except (Exception, psycopg2.Error) as error:
                    print("Erro durante a consulta de pilotos:", error)
        conn.close()
        return result
    
    def get_aeroportos_proximos_cidade(cidade):
        result = None

        conn = psycopg2.connect(**CONNECTION_PARAMS)
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                try:
                    cursor.callproc("get_aeroportos_proximos", (cidade,))
                    result = cursor.fetchall()

                except (Exception, psycopg2.Error) as error:
                    print("Erro:", error)
        conn.close()
        return result

    def get_numero_vitorias_pilotos_da_escuderia(id_escuderia):
        result = None

        conn = psycopg2.connect(**CONNECTION_PARAMS)
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                try:
                    cursor.callproc("get_numero_vitorias_pilotos_da_escuderia", (id_escuderia,))
                    result = cursor.fetchall()

                except (Exception, psycopg2.Error) as error:
                    print("Erro:", error)
        conn.close()
        return result

    def get_contagem_status_da_escuderia(id_escuderia):
        result = None

        conn = psycopg2.connect(**CONNECTION_PARAMS)
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                try:
                    cursor.callproc("get_contagem_status_da_escuderia", (id_escuderia,))
                    result = cursor.fetchall()

                except (Exception, psycopg2.Error) as error:
                    print("Erro:", error)
        conn.close()
        return result

    def get_all_vitorias_piloto(id_piloto):
        result = None

        conn = psycopg2.connect(**CONNECTION_PARAMS)
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                try:
                    cursor.callproc("get_all_vitorias_piloto", (id_piloto,))
                    result = cursor.fetchall()

                except (Exception, psycopg2.Error) as error:
                    print("Erro:", error)
        conn.close()
        return result

    def get_contagem_status_do_piloto(id_piloto):
        result = None

        conn = psycopg2.connect(**CONNECTION_PARAMS)
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                try:
                    cursor.callproc("get_contagem_status_do_piloto", (id_piloto,))
                    result = cursor.fetchall()

                except (Exception, psycopg2.Error) as error:
                    print("Erro:", error)
        conn.close()
        return result
