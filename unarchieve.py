from utils.connection import Connection
import sys


connection = Connection()
mangaId = sys.argv[1]

connection.execute("UPDATE `data` SET `status` = 1 WHERE `mangaId` = %s" % mangaId)

print("Done")