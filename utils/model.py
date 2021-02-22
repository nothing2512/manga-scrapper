class Model(object):
    def __init__(self, data):
        self.manga_id = int(data[0])
        self.name = str(data[1])
        self.logo = str(data[2])
        self.description = str(data[3])
        self.genres = str(data[4])
        self.link = str(data[5])
        self.index = int(data[6])
        self.status = int(data[7])
        self.updated = str(data[8])
        self.last = str(data[9])
