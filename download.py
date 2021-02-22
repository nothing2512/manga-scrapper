from base.downloader import Downloader as BaseDownloader


class Downloader(BaseDownloader):

    def __init__(self):
        super().__init__()
        self.status = [1, 6, 21, 26]

    @staticmethod
    def __parse_images(data):
        if "komiku.id" in data:
            data = data.split('<section id="Baca_Komik"')[1].split("</section>")[0]
            data = data.split('src="')[1:]
            images = [x.split('"')[0] for x in data]
        else:
            temp = data.split('"reading-content"')[1].split("<div class='code-block")[0].split('src="')[1:]
            images = [x.split('"')[0].replace(" \n ", "") for x in temp]
        return list(filter(None, images))


if __name__ == '__main__':
    downloader = Downloader()
    downloader.download()