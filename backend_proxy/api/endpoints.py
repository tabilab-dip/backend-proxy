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

# =============================================================


@app.route("/api/user/login", methods=["POST"])
def login_user():
    pass


@app.route("/api/user/logout", methods=["GET"])
def logout_user():
    pass


@app.route("/api/user/register", methods=["POST"])
def register_user():
    pass


@app.route("/api/user/update", methods=["POST"])
def update_user():
    pass


def get_response_json(data, status):
    return (json.dumps(data), status, {'content-type': 'application/json'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
