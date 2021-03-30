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
        ToolSchema().load(object_dict)
        """
        TODO:
        1- Get Schema dictionary
        2- Check if its enum is unique
            2.1- Implement db Class
            2.2- Implement Tool Services which uses the db Class; Check uniqueness
        3- If all fine return 200
        """
        logs = ""
        response = dict({"title": "Tool is added to the proxy",
                         "subTitle": "Logs: {}".format(logs)})
    except Exception as e:
        response = dict({"title": "500; Server Error",
                         "subTitle": "Logs: {}".format(str(e))})
    return json.dumps(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
