from flask import Flask, json, g, request, jsonify, json

app = Flask(__name__)


@app.route("/api/tools/add", methods=["POST"])
def add_tool():
    object_dict = json.loads(request.data)
    logs = "etc"
    response = dict({
                    # "status": "403",
                    "title": "403",
                    "subTitle": "Logs: {}".format(logs)})
    print(object_dict)
    print("-"*10)
    return json.dumps(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
