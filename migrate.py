from utils.connection import Connection


connection = Connection()
with open("migrate/manga.sql", "r") as f:
    for query in f.read().split(";"):
        try:
            connection.fetch(query)
        except:
            pass