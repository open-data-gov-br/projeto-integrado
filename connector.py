import mysql.connector
from dbfread import DBF
import os

try:
    path = 'files\\'
    files = os.listdir(path)

    connection = mysql.connector.connect(host='localhost',
                                         database='votacao_camara_deputados',
                                         user='root',
                                         password='medsys')
    for file_name in files:
        full_path = path + file_name

        cursor = connection.cursor()
        for record in DBF(full_path):

            values = "'" + record["NUMVOT"] + "','" + record["NOME_PAR"] + \
                "','" + record["ESTADO"] + "','" + record["VOTO"] + \
                "','" + record["PARTIDO"] + "'"

            mySql_insert_query = """INSERT INTO votos (Proposicao, Parlamentar, UF, Voto, Partido) 
                           VALUES (""" + values + """) """
            print(mySql_insert_query)

            cursor.execute(mySql_insert_query)
            connection.commit()

        cursor.close()

except mysql.connector.Error as error:
    print("Failed to insert record into votos table {}".format(error))

finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")
