from utils.connection import Connection
from utils.model import Model
from datetime import datetime, date
import requests


class Checker(Connection):

    def __init__(self):
        super().__init__()
        self.__named = []
        self.__error = []
        self.__paused = []
        self.__unpaused = []
        self.__ended = []

    def get_data(self):
        return []

    @staticmethod
    def is_end(data):
        try:
            data = data.replace("\"", "'").lower().strip()
            ended = data.split("new1 sd rd")[2].split("</div>")[0].split("</span")[-2].split("<span>")[-1]
            return "- end" in ended or "-end" in ended
        except:
            return False

    @staticmethod
    def is_paused(data):
        try:
            last = data.split('<td class="tanggalseries">')[1].split("</td>")[0].strip()
            if "lalu" in last:
                num = int(last[0])

                return "bulan" in last and num > 2
            else:
                last = last.split("/")
                now = date.today()
                last = date(int(last[2]), int(last[1]), int(last[0]))
                delta = now - last
                return delta.days > 60
        except:
            return False

    def check(self):
        data = self.get_data()
        size = len(data)
        updated = 0
        i = 0

        for x in data:
            i += 1
            model = Model(x)
            try:
                print(("Getting data %d/%d: %s%s" % (i, size, model.name, " " * 30)).strip(), end="\r")
                updated += self.__get_episodes(model)
            except:
                self.__error.append(model.name + (" " * 100))

        print()
        print("Total Manga Updated: %d%s" % (len(self.__named), " " * 60))
        print("Total Updated: %d%s" % (updated, " " * 60))

        if len(self.__paused) > 0:
            print()
            print("Paused: ")
            for x in self.__paused:
                print(x.strip())

        if len(self.__unpaused) > 0:
            print()
            print("Unpaused: ")
            for x in self.__unpaused:
                print(x.strip())

        if len(self.__ended) > 0:
            print()
            print("Ended: ")
            for x in self.__ended:
                print(x.strip())

        if len(self.__error) > 0:
            print()
            print("Error: ")
            for x in self.__error:
                print(x.strip())

        print()
        print("Updated: ")
        if len(self.__named) == 0:
            self.__named.append("No updates")
        for x in self.__named:
            print(x)

        print()
        print("Last Checked: ", datetime.now().strftime("%H:%M:%S"))

    def __update(self, model):
        query = "UPDATE `data` SET `index` = %d WHERE `mangaId` = %d"
        self.execute(query % (model.index, model.manga_id))

    def __insert(self, manga_id, data):
        query = "INSERT INTO `queued`(`mangaId`, `link`) VALUES ('%d', '%s')"
        for x in data:
            self.execute(query % (manga_id, x))

    def __check_status(self, data, model):
        paused = self.is_paused(data)
        ended = self.is_end(data)

        if paused and model.status != 21:
            self.__paused.append(model.name)
            self.execute("UPDATE `data` SET `status` = 21 WHERE `mangaId` = %d" % model.manga_id)
        elif not paused and model.status == 21:
            self.__unpaused.append(model.name)
            self.execute("UPDATE `data` SET `status` = 1 WHERE `mangaId` = %d" % model.manga_id)

        if ended:
            self.__ended.append(model.name)
            self.execute("UPDATE `data` SET `status` = 6 WHERE `mangaId` = %d" % model.manga_id)

    def __get_episodes(self, model):
        req = requests.get(model.link)
        data = self.__parse_episode(req.text)
        self.__check_status(req.text, model)
        index = model.index + 1
        model.index = len(data) - 1
        data = data[index:]
        if len(data) > 0:
            self.__update(model)
            self.__insert(model.manga_id, data)
            self.__named.append(model.name)
        return len(data)

    @staticmethod
    def __parse_episode(link):
        return []
