import copy


class Environment:
    def __init__(self, store, name):
        self.name = name
        self.dict = {}
        self.store = store

    def define(self, name):
        id = self.store.make_variable(name)
        self.dict[name] = id

    def assign(self, name, value):
        if name in self.dict:
            id = self.dict[name]
            self.store.assign(id, value)
        else:
            print("ERROR: variable " + name + " not found")

    def copy(self):
        new = Environment(self.store, self.name)
        new.dict = copy.deepcopy(self.dict)
        return new

    def get(self, name):
        if name in self.dict:
            id = self.dict[name]
            value = self.store.get(id)
            return value
        else:
            print("ERROR: variable " + name + " not found")

    def __str__(self):
        return "ENVIRONMENT " + ":" + str(self.dict)
