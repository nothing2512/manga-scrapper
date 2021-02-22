from utils.connection import Connection
import sys


connection = Connection()
mangaId = sys.argv[1]

connection.execute("UPDATE `data` SET `index` = -1 WHERE `mangaId` = %s" % mangaId)
connection.execute("DELETE FROM `queued` WHERE mangaId = %s" % mangaId)
connection.execute("DELETE FROM `chapter_image` WHERE `chapterId` IN (SELECT `chapterId` FROM `chapter` WHERE `mangaId` = %s)" % mangaId)
connection.execute("DELETE FROM `chapter` WHERE `mangaId` = %s" % mangaId)

print("Done")