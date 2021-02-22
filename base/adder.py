from utils.connection import Connection
from utils.constants import *
import requests
from urllib.parse import unquote
from datetime import datetime


class Adder(Connection):

    def __init__(self):
        super().__init__()
        self.status = 1

    def add(self, link, idx=None):

        title = [x for x in link.split("/") if x != ""][-1].replace("-", " ")
        link = unquote(link.strip())
        req = requests.get(link)
        data = req.text

        chapters, index, logo_url = self.__parse_data(data)
        logo_url = unquote(logo_url)
        logo = self.__download_logo(logo_url)
        now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        
        older = self.fetchall("SELECT * FROM `data` WHERE `link` = '%s'" % link)
        sinopsis = self.get_sinopsis(data)
        genres = self.get_genre(data)

        if len(older) == 0:
            query = "INSERT INTO `data`(`name`, `logo`, `description`, `genres`, `link`, `index`, `status`, `updated`) "
            query += "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', %d, '%s')"

            self.execute(query % (title, logo, sinopsis, genres, link, index, self.status, now))
            manga_id = self.lastinsertid()

            if idx is None:
                self.__insert_chapters(manga_id, chapters)
            else:
                self.__insert_chapters(manga_id, chapters[(int(idx) - 1):])

            print()
            print("Finish Add %s" % title)
            print("Updated %d" % len(chapters))
        else:
            manga = older[0]
            if manga[4] in [0, 3]:
                print("Manga has been added")
                print("do you want to unarchieve it ?")
                x = input()
                if x in ["y", "yes", "Y", "Yes", "YES"]:
                    status = 0 if manga[4] == 0 else 2
                    self.execute("UPDATE `data` SET `status` = %d WHERE `mangaId` = %d" %(status, manga[0]))
            else:
                print("Manga has been added and not archieved")

    def __insert_chapters(self, manga_id, chapters):
        query = "INSERT INTO `queued`(`mangaId`, `link`) VALUES ('%d', '%s')"
        for x in chapters:
            self.execute(query % (manga_id, x))

    @staticmethod
    def __download_logo(link):
        link = link.strip()
        img = requests.get(link, stream=True)
        length = img.headers.get("content-length")
        ext = link.split("?")[0].split(".")[-1]
        filename = datetime.now().strftime("%Y%m%d%H%M%S") + "." + ext
        with open(LOGO_DIR + filename, "wb") as f:
            if length is None:
                print("[INFO] logo size: 0kb")
                f.write(img.content)
            else:
                dl = 0
                length = int(length)
                content_length = "{:.2f}".format(length / 1024)
                print("[INFO] logo size: %s kb" % content_length)
                for i in img.iter_content(chunk_size=1024):
                    dl += len(i)
                    f.write(i)
                    percent = "{:.2f}".format(dl * 100 / length)
                    print("[INFO] Download progress: %s%s" % (percent, "%"), end="\r")
        return LOGO_TEMP % filename

    @staticmethod
    def get_genre(data):
        try:
            if "komiku.id" in data:
                genre = data.replace("\"", "'").split("<ul class='genre'>")[1].split("</ul>")[0].split("</a>")
                genre = [x.split(">")[-1].strip() for x in genre[:-1]]
                return ", ".join(genre)
            else:
                genre = data.split("genres-content")[1].split("</div>")[0].split("</a>")
                genre = [x.split(">")[-1] for x in genre]
                return ", ".join(genre)
        except:
            return ""

    @staticmethod
    def get_sinopsis(data):
        try:
            if "komiku.id" in data:
                sinopsis = data.replace("\"", "'").split("id='Sinopsis'")[1].split("</h3>")[1].split("<h2>")[0].strip()
                sinopsis = sinopsis.replace("\r", "").replace("\n", "<br>")
                sinopsis = sinopsis.replace("</p><p>", "<br>").replace("<p>", "").replace("</p>", "")
                return sinopsis.replace("'", "").replace("\"", "")
            else:
                return data.split("summary__content")[1].split("<p>")[1].split("</p>")[0]
        except:
            return ""

    @staticmethod
    def __parse_data(data):
        return [], 0, ""
