from backend_proxy.db.mongoDB import MongoDB
from backend_proxy.tool.schema import ToolSchema, dtime_format
import backend_proxy.misc.util as util
import backend_proxy.misc.conllXtostandoff as conllXtostandoff
import datetime as dt
import requests

# dt.datetime.now()


class Service:
    def __init__(self):
        self.db = MongoDB()

    def add_tool(self, req_dict):
        enum = req_dict["enum"]
        if self.enum_exists(enum):
            raise Exception("The enum: {} already exists, "
                            "enter a unique one".format(enum))
        author_json, form_data_json, root_json = util.get_specs_from_git(
            req_dict["git"])
        req_dict["author_json"] = author_json
        req_dict["root_json"] = root_json
        req_dict["form_data_json"] = form_data_json
        req_dict["update_time"] = dt.datetime.now()
        self.db.create(req_dict)
        return self.dump(req_dict)

    def update_tool(self, req_dict, original_enum):
        enum = req_dict["enum"]
        if self.enum_exists(enum) and (enum != original_enum):
            raise Exception("The enum: {} already exists, "
                            "enter a unique one".format(enum))
        # Reloads the git URL again since
        #   this might be the main motivation of the update
        author_json, form_data_json, root_json = util.get_specs_from_git(
            req_dict["git"])
        req_dict["author_json"] = author_json
        req_dict["root_json"] = root_json
        req_dict["form_data_json"] = form_data_json
        req_dict["update_time"] = dt.datetime.now()
        self.db.update({"enum": original_enum}, req_dict)
        return self.dump(req_dict)

    def delete_tool(self, enum):
        tool_dict = self.db.find({"enum": enum})
        if tool_dict is None:
            raise Exception("Tool enum does not exist")
        self.db.delete(tool_dict)
        return self.dump(tool_dict)

    def get_tool_ui_info(self, enum):
        tool_dict = self.db.find({"enum": enum})
        if tool_dict is None:
            raise Exception("Tool with enum: {} does not exist".format(enum))
        tool_dict = ToolSchema(only=(
            "author_json", "root_json", "form_data_json")).dump(tool_dict)
        return tool_dict

    def run_tool(self, enum, input_dict):
        tool_dict = self.db.find({"enum": enum})
        if tool_dict is None:
            raise Exception("Tool with enum: {} does not exist".format(enum))
        tool_dict = self.dump(tool_dict)
        ip, port = tool_dict["ip"], tool_dict["port"]
        response = self.run_request(ip, port, input_dict).json()
        if "brat_conll" in response:
            standoff = conllXtostandoff.process(response["brat_conll"])
            response["brat_standoff"] = standoff
            del response["brat_conll"]
        return response

    def list_all_tools(self):
        tools = self.db.find_all()
        return [ToolSchema(only=("enum", "name", "ip", "port", "git", "update_time"))
                .dump(tool)
                for tool in tools]

    def get_tool_names(self):
        tools = self.db.find_all()
        return [ToolSchema(only=("enum", "name")).dump(tool) for tool in tools]

    def enum_exists(self, enum):
        return (self.db.find({"enum": enum}) is not None)

    def dump(self, obj):
        return ToolSchema(exclude=['_id']).dump(obj)

    def run_request(self, ip, port, input_dict):
        # all running programs must implement /evaluate endpoint
        addr = "http://{}:{}/evaluate".format(ip, port)
        return requests.post(addr, json=input_dict)
