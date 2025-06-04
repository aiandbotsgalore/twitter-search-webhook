from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")

@app.route("/twittersearch", methods=["POST"])
def twitter_search():
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

    params = {
        "query": query,
        "max_results": 5,
        "tweet.fields": "author_id,text,created_at"
    }

    url = "https://api.twitter.com/2/tweets/search/recent"
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return jsonify({"error": "Twitter API error", "details": response.text}), 500

    tweets = response.json().get("data", [])
    return jsonify({"results": tweets})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
