from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)
FASTAPI_URL = "http://localhost:8000/api/cpes"

@app.template_filter('format_date')
def format_date(value):
    if not value:
        return ""
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%b %d, %Y")
    except Exception:
        return value

@app.route("/", methods=["GET"])
def index():
    # Default query params
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=15, type=int)

    filters = {
        "cpe_title": request.args.get("cpe_title"),
        "cpe_22_uri": request.args.get("cpe_22_uri"),
        "cpe_23_uri": request.args.get("cpe_23_uri"),
        "deprecation_date": request.args.get("deprecation_date"),
        "page": page,
        "limit": limit
    }

    query_params = {k: v for k, v in filters.items() if v}

    try:
        if any(k in query_params for k in ["cpe_title", "cpe_22_uri", "cpe_23_uri", "deprecation_date"]):
            response = requests.get(f"{FASTAPI_URL}/search", params=query_params)
        else:
            response = requests.get(f"{FASTAPI_URL}", params=query_params)

        response.raise_for_status()
        data = response.json()
        cpes = data["data"]
        total = data.get("total", len(cpes))
    except Exception as e:
        print("API error:", e)
        cpes = []
        total = 0

    return render_template("index.html", cpes=cpes, filters=filters, page=page, limit=limit, total=total)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
