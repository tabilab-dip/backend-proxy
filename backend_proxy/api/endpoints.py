from flask import Flask, json, g, request, jsonify, json, session
from backend_proxy.tool.schema import ToolSchema
from backend_proxy.tool.service import ToolService
from backend_proxy.user.service import UserService
from backend_proxy.api.exception import REST_Exception
from backend_proxy.db.mongoDB import MongoDB
from datetime import timedelta
from backend_proxy.misc.util import *
import traceback

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=5)
app.secret_key = "TODO"


# Auth is needed and roles specify the output
@app.route("/api/tools", methods=["GET"])
def list_all_tools():
    try:
        access_tools = UserService().get_tools_user(session)
        data = ToolService().list_all_tools(access_tools)
        status = 200
    except REST_Exception as e:
        traceback.print_exc()
        data = dict({"title": "Server Error",
                     "subTitle": "Logs: {}".format(str(e))})
        status = e.status
    return get_response_json(data, status)

# Auth is not needed


@app.route("/api/tools/name", methods=["GET"])
def get_tool_names():
    try:
        data = ToolService().get_tool_names()
        status = 200
    except REST_Exception as e:
        data = dict({"title": "Server Error",
                     "subTitle": "Logs: {}".format(str(e))})
        status = e.status
    return get_response_json(data, status)

# Auth is needed


@app.route("/api/tool", methods=["POST"])
def add_tool():
    try:
        UserService().assert_logged_in(session)
        req_dict = json.loads(request.data)
        req_dict = ToolService().add_tool(req_dict)
        UserService().add_tool_to_user(session, req_dict["enum"])
        data = dict({"title": "Tool is added to the proxy",
                     "subTitle": "Tool Info: {}".format(json.dumps(req_dict))})
        status = 200
    except REST_Exception as e:
        traceback.print_exc()
        data = dict({"title": "Server Error",
                     "subTitle": "Logs: {}".format(str(e))})
        status = e.status
    return get_response_json(data, status)


# Auth is needed and roles matter
@app.route("/api/tool/<enum>", methods=["PUT"])
def update_tool(enum):
    try:
        access_tools = UserService().get_tools_user(session)
        req_dict = json.loads(request.data)
        req_dict = ToolService().update_tool(req_dict, enum, access_tools)
        data = dict({"title": "Tool is updated",
                     "subTitle": "Tool Info: {}".format(json.dumps(req_dict))})
        status = 200
    except REST_Exception as e:
        data = dict({"title": "Server Error",
                     "subTitle": "Logs: {}".format(str(e))})
        status = e.status
    return get_response_json(data, status)

# Auth is needed and roles matter


@app.route("/api/tool/<enum>", methods=["DELETE"])
def delete_tool(enum):
    try:
        access_tools = UserService().get_tools_user(session)
        tool_json = ToolService().delete_tool(enum, access_tools)
        data = dict({"title": "Tool is deleted",
                     "subTitle": "Tool Info: {}".format(json.dumps(tool_json))})
        status = 200
    except REST_Exception as e:
        data = dict({"title": "Server Error",
                     "subTitle": "Logs: {}".format(str(e))})
        status = e.status
    return get_response_json(data, status)

# Auth is not needed


@app.route("/api/tool/ui/<enum>", methods=["GET"])
def get_tool_ui_info(enum):
    try:
        data = ToolService().get_tool_ui_info(enum)
        status = 200
    except REST_Exception as e:
        data = dict({"title": "Server Error",
                     "subTitle": "Logs: {}".format(str(e))})
        status = e.status
    return get_response_json(data, status)

# Auth is not neeed


@app.route("/api/tool/run/<enum>", methods=["POST"])
def run_tool(enum):
    print("halooo")
    try:
        # input for the tool
        input_dict = json.loads(request.data)
        data = ToolService().run_tool(enum, input_dict)
        status = 200
    except REST_Exception as e:
        traceback.print_exc()
        data = dict({"title": "Server Error",
                     "subTitle": "Logs: {}".format(str(e))})
        status = e.status
    return get_response_json(data, status)

# =============================================================


@app.route("/api/user/login", methods=["POST"])
def login_user():
    session.clear()
    try:
        req_dict = json.loads(request.data)
        user = UserService().login_user(req_dict)
        # login succeeded gen session
        session["username"] = user["username"]
        data = dict({"title": "Login success", })
        status = 200
    except REST_Exception as e:
        data = dict({"title": "Server Error",
                     "subTitle": "Logs: {}".format(str(e))})
        status = e.status
    return get_response_json(data, status)


@app.route("/api/user/logout", methods=["GET"])
def logout_user():
    session.clear()
    data = dict({"title": "Logged out"})
    status = 200
    return get_response_json(data, status)


@app.route("/api/user/register", methods=["POST"])
def register_user():
    try:
        req_dict = json.loads(request.data)
        user = UserService().register_user(req_dict, session)
        data = dict({"title": "Register success", })
        status = 200
    except REST_Exception as e:
        data = dict({"title": "Server Error",
                     "subTitle": "Logs: {}".format(str(e))})
        status = e.status
    return get_response_json(data, status)


@app.route("/api/user/update", methods=["POST"])
def update_user():
    try:
        req_dict = json.loads(request.data)
        user = UserService().update_user(req_dict, session)
        data = dict({"title": "Update success", })
        status = 200
    except REST_Exception as e:
        data = dict({"title": "Server Error",
                     "subTitle": "Logs: {}".format(str(e))})
        status = e.status
    return get_response_json(data, status)


def get_response_json(data, status):
    return (json.dumps(data), status, {'content-type': 'application/json'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
