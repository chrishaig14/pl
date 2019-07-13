from colorama import Fore

class Store:
    def make_variable(self, name):
        if name not in self.names_dict:
            self.names_dict[name] = 0
        else:
            self.names_dict[name] += 1

        id = name + "(" + str(self.names_dict[name]) + ")"
        self.dict[id] = None
        return id

    def __init__(self):
        self.dict = {}
        self.names_dict = {}

    def assign(self, id, value):
        self.dict[id] = value

    def get(self, id):
        if id in self.dict:
            return self.dict[id]
        return self.dict[id]

    def __str__(self):
        return "STORE:" + str(self.dict)
