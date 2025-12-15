from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/prices")
def api_prices():
    """
    GET /api/prices?query=iphone+15+pro+max

    CURRENT: demo prices + real Amazon / Flipkart search URLs.
    LATER: replace prices[] with real Amazon / Flipkart API or scraping logic.
    """
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"error": "query required"}), 400

    base_price = 157499  # demo base (iPhone‑style)

    prices = [
        {
            "store": "Flipkart",
            "price": base_price,
            "shipping": "Free",
            "status": "In Stock",
            "url": f"https://www.flipkart.com/search?q={query}"
        },
        {
            "store": "Amazon",
            "price": base_price + 2500,
            "shipping": "Free",
            "status": "In Stock",
            "url": f"https://www.amazon.in/s?k={query}"
        }
    ]

    min_price = min(p["price"] for p in prices)
    for p in prices:
        p["best"] = (p["price"] == min_price)

    return jsonify({"query": query, "prices": prices})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
