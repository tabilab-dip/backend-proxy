from backend_proxy.db.mongoDB import MongoDB
from backend_proxy.tool.schema import ToolSchema, dtime_format
import backend_proxy.misc.util as util
import datetime as dt
import requests


class UserService:
    def __init__(self):
        self.db = MongoDB()

    def login_user(self, req_dict):
        pass

    def logout_user(self, token):
        pass

    def register_user(self, req_dict):
        pass

    def update_user(self, req_dict, token):
        pass
