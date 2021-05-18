import mysql.connector

def conectar():
    try:
        database = mysql.connector.connect(
            host = "localhost",
            port = 3308,
            user = "root",
            password = "",
            database = "sys_inscripciones")
    except:
        database = mysql.connector.connect(
            host = "localhost",
            port = 3308,
            user = "root",
            password = "")

        try:
            generarDB(database)
        except:
            print("Ocurrió un error al generar la base de datos.")
            raise 

    cursor = database.cursor(buffered = True)
    return[database,cursor]

def generarDB(database):
    sql_file = open("database.sql")
    sql_as_string = sql_file.read()
    sql_file.close()
    sqlCommands = sql_as_string.split(';')

    for command in sqlCommands:
        database.cursor().execute(command)

    print(f"Se ha generado la base de datos.")