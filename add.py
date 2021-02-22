import sys
from base.adder import Adder as BaseAdder


class Adder(BaseAdder):

    def __init__(self):
        super().__init__()
        self.status = 1

    @staticmethod
    def __parse_data(data):
        if "komiku.id" in data:
            m_data = data.split('<th class="judulseries">')[1].split('<a href="/ch')[1:]
            chapters = ["https://komiku.id/ch" + x.split('"')[0] for x in m_data]
            logo = data.split("<div class=\"ims\"><img src=\"")[1].split("\"")[0]
        else:
            m_data = data.split("listing-chapters_wrap")[1].split("</ul>")[0].split("<li")[1:]
            chapters = [x.split('href="')[1].split('"')[0] + "?style=list" for x in m_data]
            logo = data.split("summary_image")[1].split('src="')[1].split('"')[0]

        index = len(chapters) - 1

        return chapters[::-1], index, logo


if __name__ == '__main__':
    uri = sys.argv[1]
    if len(sys.argv) > 2:
        indexes = sys.argv[2]
    else:
        indexes = None
    adder = Adder()
    adder.add(uri, indexes)
