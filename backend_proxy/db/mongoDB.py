from pymongo import MongoClient

# TODO
url = ""


class MongoDB(object):
    def __init__(self):
        # TODO: use local db for now
        self.db = MongoClient(host="localhost", port=27017).tools

    def find_all(self, query):
        return self.db.tools.find(query)

    def find(self, query):
        return self.db.tools.find_one(query)

    def create(self, tool):
        return self.db.tools.insert_one(tool)

    def update(self, query, tool):
        return self.db.tools.replace_one(query, tool).modified_count

    def delete(self, query):
        return self.db.tools.delete_one(query).deleted_count
