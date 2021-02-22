from base.checker import Checker as BaseChecker
import sys


class Checker(BaseChecker):

    def __init__(self, c_all=False):
        super().__init__()
        self.c_all = c_all

    def get_data(self):
        query = "SELECT * FROM `data` WHERE `status` = 1 OR `status` = 21" if self.c_all \
            else "SELECT * FROM `data` WHERE `status` = 1"
        return self.fetchall(query)

    @staticmethod
    def __parse_episode(data):
        if "komiku.id" in data:
            data = data.split('<th class="judulseries">')[1].split('<a href="/ch')[1:]
            episodes = ["https://komiku.id/ch" + x.split('"')[0] for x in data]
        else:
            temp = data.split("listing-chapters_wrap")[1].split("</ul>")[0].split("<li")[1:]
            episodes = [x.split('href="')[1].split('"')[0] + "?style=list" for x in temp]

        return episodes[::-1]


if __name__ == '__main__':
    check = Checker(len(sys.argv) > 1)
    check.check()
