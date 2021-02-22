import os

import requests
from utils.model import Model
from utils.constants import *
from utils.connection import Connection
from datetime import datetime


class Downloader(Connection):

    def __init__(self):
        super().__init__()
        self.__total_download = 0
        self.__filename = datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.__ch_index = 0
        self.__emid = []
        self.status = None

    def __get_filename(self, url):
        ext = url.split("?")[0].split(".")[-1]
        filename = self.__filename + str(self.__ch_index) + "." + ext
        self.__ch_index += 1
        if filename[-1] == ".":
            filename += "jpg"
        if len(ext) > 5:
            filename = self.__filename + str(self.__ch_index) + ".jpg"
        return filename

    @staticmethod
    def __parse_images(data):
        return []

    @staticmethod
    def __show_log(x, name, total_image, x_manga, total_manga):
        messages = [
            #"[INFO] download proccess limit 100 chapters",
            "[INFO] Download manga: " + name,
            "[INFO] Manga progress: " + str(x_manga) + "/" + str(total_manga),
            "[INFO] Manga Remain  : " + str(total_manga - x_manga + 1),
            "[INFO] Image progress: " + str(x) + "/" + str(total_image + 1)
        ]
        print("\n".join(messages))

    def __single(self, manga_id, link, i, size, chapter_id):
        manga = Model(self.fetch("SELECT * FROM `data` WHERE `mangaId` = %d" % manga_id))
        print("Get data from: %s" % manga.name)

        data = requests.get(link)
        images = self.__parse_images(data.text)

        x = 1
        total_image = len(images) - 1
        for item in images:
            filename = self.__get_filename(item)
            os.system("cls")
            self.__show_log(x, manga.name, total_image, i, size)
            with open(CH_DIR + filename, "wb") as f:
                img = requests.get(item, stream=True)
                length = img.headers.get("content-length")
                if length is None:
                    print("[INFO] image size: 0 kb")
                    f.write(img.content)
                    f.close()
                else:
                    dl = 0
                    length = int(length)
                    self.__total_download += length
                    content_length = "{:.2f}".format(length / 1024)
                    print("[INFO] image size: %s kb" % content_length)
                    for c in img.iter_content(chunk_size=1024):
                        dl += len(c)
                        f.write(c)
                        percent = "{:.2f}".format(dl * 100 / length)
                        print("[INFO] Download progress: %s%s" % (percent, "%"), end="\r")
            ch_dir = CH_TEMP % filename
            self.execute("INSERT INTO `chapter_image`(`chapterId`, `image`) VALUES (%d, '%s')" % (chapter_id, ch_dir))
            x += 1

    def download(self):
        first_time = datetime.now()
        self.execute("DELETE FROM `chapter` WHERE `status` = 0")
        data = []
        if isinstance(self.status, int):
            query = "SELECT * FROM `queued` WHERE `status` = 0 AND `mangaId` IN "\
                    "(SELECT `mangaId` FROM `data` WHERE `status` = %d) ORDER BY `queuedId` ASC"
            data = self.fetchall(query % self.status)
        else:
            for status in self.status:
                query = "SELECT * FROM `queued` WHERE `status` = 0 AND `mangaId` IN " \
                        "(SELECT `mangaId` FROM `data` WHERE `status` = %d) ORDER BY `queuedId` ASC"
                data.append(self.fetchall(query % status))
        size = len(data)
        i = 1
        for x in data:
            now = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
            queued_id = x[0]
            manga_id = x[1]
            link = x[2]

            if manga_id not in self.__emid:
                self.execute("INSERT INTO `chapter`(`mangaId`, `page`, `status`) VALUES(%d, %d, 0)" % (manga_id, i))
                chapter_id = self.lastinsertid()

                # try:
                self.__single(manga_id, link, i, size, chapter_id)
                self.execute("UPDATE `queued` SET `status` = 1 WHERE `queuedId` = %d" % queued_id)
                self.execute("UPDATE `data` SET `updated` = '%s' WHERE `mangaId` = %d" % (now, manga_id))
                self.execute("UPDATE `chapter` SET `status` = 1 WHERE `chapterId` = %d" % chapter_id)
                # except:
                #     self.__emid.append(manga_id)

            i += 1
        self.execute("DELETE FROM `queued` WHERE `status` = 1")

        kbs = self.__total_download / 1000
        mb = int(kbs / 1024)
        kb = int(kbs % 1024)
        print()
        print("Total Downloaded: {:d} MB {:d} KB".format(mb, kb))

        last_time = datetime.now()
        diff = last_time - first_time
        seconds = diff.total_seconds()
        speed = int(kbs / seconds)
        minutes = seconds / 60
        seconds = seconds % 60

        print()
        print("Total Time: %d Minutes %d Seconds" % (minutes, seconds))
        print("Total Speed: %d kb/s" % speed)
