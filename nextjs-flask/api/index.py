from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv("..")

# app instance
app = Flask(__name__)
CORS(app)

@app.route("/api/search", methods=["GET"])
def return_home():
    query = request.args.getlist("query")
    query_params = query[0].split(" ")
    length = int(request.args.getlist("length")[0])
    # result = search.main(query_params, host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"], password=os.environ["REDIS_PASS"])
    result = []
    ex = ("url", "title")
    result.append(ex)
    result_dict = dict()
    removed_links = 0
    for i in range(len(result)):
        if i - removed_links >= length:
            break
        url, title = result[i]
        result_dict[i - removed_links] = [url, title]
    return jsonify({
        "result" : result_dict
    })


if __name__ == "__main__":
    app.run()