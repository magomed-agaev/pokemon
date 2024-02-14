import requests


class Move():

    def __init__(self, url):

        # call the moves API endpoint
        req = requests.get(url)
        self.json = req.json()

        self.name = self.json['name']
        self.power = self.json['power']
        self.type = self.json['type']['name']
