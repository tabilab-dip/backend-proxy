from backend_proxy.db.mongoDB import MongoDB
from backend_proxy.tool.schema import ToolSchema, dtime_format
import backend_proxy.misc.util as util
import datetime as dt
import requests


class UserService:
    def __init__(self):
        self.db = MongoDB()
