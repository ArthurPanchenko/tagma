from peewee import PostgresqlDatabase


db = PostgresqlDatabase(
    'tagmaV1',
    user='admin',
    password='admin',
    host='localhost',
    port='5432'
)