from flask import Flask, json, g, request, jsonify, json
from backend_proxy.tool.schema import ToolSchema
from util import *
app = Flask(__name__)


@app.route("/api/tools/add", methods=["POST"])
def add_tool():
    try:
        check_is_auth(request)
        object_dict = json.loads(request.data)
        git_url = object_dict["git"]
        author_json, form_data_json, root_json = get_specs_from_git(git_url)
        object_dict["author_json"] = author_json
        object_dict["root_json"] = root_json
        object_dict["form_data_json"] = form_data_json
        tool_schema = ToolSchema().load(object_dict)
        logs = ""
        response = dict({"title": "Tool is added to the proxy",
                         "subTitle": "Logs: {}".format(logs)})
    except Exception as e:
        response = dict({"title": "500; Server Error",
                         "subTitle": "Logs: {}".format(str(e))})
    return json.dumps(response)


"""
list endpoints:
Step 1 - Dynamic System:
1- POST: add_tool:
    given a tool description, add it to the database; the tool's enum must be unique
2- GET: list all tools with all of their information
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

"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
