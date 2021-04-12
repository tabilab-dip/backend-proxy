from pymongo import MongoClient

# TODO
url = ""


class MongoDB(object):
    def __init__(self, col):
        # TODO: use local db for now
        self.db = MongoClient(host="localhost", port=27017).tools
        self.col = col

    def find_all(self):
        return self.db[self.col].find({})

    def find(self, query):
        return self.db[self.col].find_one(query)

    def create(self, tool):
        return self.db[self.col].insert_one(tool)

    def update(self, query, tool):
        return self.db[self.col].replace_one(query, tool).modified_count

    def delete(self, query):
        return self.db[self.col].delete_one(query).deleted_count
