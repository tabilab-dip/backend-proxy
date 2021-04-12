from flask import Flask, json, g, request, jsonify, json
from backend_proxy.tool.schema import ToolSchema
from backend_proxy.tool.service import ToolService
from backend_proxy.db.mongoDB import MongoDB
from backend_proxy.misc.util import *
import traceback

app = Flask(__name__)


@app.route("/api/tools", methods=["GET"])
def list_all_tools():
    try:
        data = ToolService().list_all_tools()
        status = 200
    except Exception as e:
        traceback.print_exc()
        data = dict({"title": "500; Server Error",
                     "subTitle": "Logs: {}".format(str(e))})
        status = 500
    return get_response_json(data, status)


@app.route("/api/tools/name", methods=["GET"])
def get_tool_names():
    try:
        data = ToolService().get_tool_names()
        status = 200
    except Exception as e:
        data = dict({"title": "500; Server Error",
                     "subTitle": "Logs: {}".format(str(e))})
        status = 500
    return get_response_json(data, status)


@app.route("/api/tool", methods=["POST"])
def add_tool():
    try:
        req_dict = json.loads(request.data)
        req_dict = ToolService().add_tool(req_dict)
        data = dict({"title": "Tool is added to the proxy",
                     "subTitle": "Tool Info: {}".format(json.dumps(req_dict))})
        status = 200
    except Exception as e:
        traceback.print_exc()
        data = dict({"title": "500; Server Error",
                     "subTitle": "Logs: {}".format(str(e))})
        status = 500
    return get_response_json(data, status)


@app.route("/api/tool/<enum>", methods=["PUT"])
def update_tool(enum):
    try:
        req_dict = json.loads(request.data)
        req_dict = ToolService().update_tool(req_dict, enum)
        data = dict({"title": "Tool is updated",
                     "subTitle": "Tool Info: {}".format(json.dumps(req_dict))})
        status = 200
    except Exception as e:
        data = dict({"title": "500; Server Error",
                     "subTitle": "Logs: {}".format(str(e))})
        status = 500
    return get_response_json(data, status)


@app.route("/api/tool/<enum>", methods=["DELETE"])
def delete_tool(enum):
    try:
        tool_json = ToolService().delete_tool(enum)
        data = dict({"title": "Tool is deleted",
                     "subTitle": "Tool Info: {}".format(json.dumps(tool_json))})
        status = 200
    except Exception as e:
        data = dict({"title": "500; Server Error",
                     "subTitle": "Logs: {}".format(str(e))})
        status = 500
    return get_response_json(data, status)


@app.route("/api/tool/ui/<enum>", methods=["GET"])
def get_tool_ui_info(enum):
    try:
        data = ToolService().get_tool_ui_info(enum)
        status = 200
    except Exception as e:
        data = dict({"title": "500; Server Error",
                     "subTitle": "Logs: {}".format(str(e))})
        status = 500
    return get_response_json(data, status)


@app.route("/api/tool/run/<enum>", methods=["POST"])
def run_tool(enum):
    print("halooo")
    try:
        # input for the tool
        input_dict = json.loads(request.data)
        data = ToolService().run_tool(enum, input_dict)
        status = 200
    except Exception as e:
        traceback.print_exc()
        data = dict({"title": "500; Server Error",
                     "subTitle": "Logs: {}".format(str(e))})
        status = 500
    return get_response_json(data, status)


def get_response_json(data, status):
    return (json.dumps(data), status, {'content-type': 'application/json'})


"""
list endpoints:
Step 0 - Move logic etc to service
Step 1 - Dynamic System:
1- POST: add_tool:
    given a tool description, add it to the database; the tool's enum must be unique
2- GET: list_all_tools 
    list all with all of their information
    return all of the tools with all of their information
3- UPDATE: update_tool:
    given a tool description, find the one with the same enum, and update it
        - this does not update the enum, since it is unique, returns error if enum does not exist
        - hence, frontend should not let user try to edit it in the first place
4- DELETE: delete_tool:
    given a tool description, delete it: only enum is enough
5- GET: get_tool_names:
    return names and enums of all of the tools in the db, don't return any other info,
    no input requried here, just return 
6- GET: get_tool_ui_info: 
    given an enum, return the author_json, root_json, form_data_json fields
7- POST: run_tool:
    given enum of a tool
    retrieves the tool's info, make HTTP request to that IP:PORT,
    get back the info, and depending on brat format do further 
        parsing in the parsing to get standoff format


Step 2 - Authentication:
1- Login
    - required endpoints for authentication, and update the existing endpoints to check for that.
    - update password etc.
    - timely session
    - update DB class to load initial passwd from OS environ variable

"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
