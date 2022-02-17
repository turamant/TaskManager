import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Establishing a connection with postgres
connection = psycopg2.connect(user="postgres", password="postgres")
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Creating a cursor to perform operations with the database
cursor = connection.cursor()
sql_create_database = cursor.execute('create database task1')
# Closing the connection
cursor.close()
connection.close()
