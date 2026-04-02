from flask import Flask, request, render_template, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__, static_url_path='', static_folder='.', template_folder='.')

# Enable CORS for all routes
CORS(app)

# Load NIC training data
try:
    df = pd.read_csv("nic_training_dataset.csv")
    descriptions = df["Business_Description"]
    nic_codes = df["NIC_code"].astype(str)
    
    vectorizer = TfidfVectorizer()
    X_vec = vectorizer.fit_transform(descriptions)
    print("Training data loaded successfully")
except Exception as e:
    print(f"Error loading training data: {e}")
    df = pd.DataFrame()
    descriptions = []
    nic_codes = []
    X_vec = None

# Keyword-based overrides
KEYWORD_NIC_OVERRIDES = [
    {
        "keywords": ["mobile app", "android app", "ios app", "iphone app", "mobile application"],
        "nic_code": "621100",
    },
    {
        "keywords": [
            "eco friendly cleaning",
            "eco-friendly cleaning", 
            "green cleaning powder",
            "cleaning powder",
            "detergent powder",
            "household cleaning powder",
        ],
        "nic_code": "202303",
    },
]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict", methods=["POST"])
def predict():
    desc = request.form.get("description") or (request.json.get("description") if request.is_json else "")

    if not desc or not desc.strip():
        return jsonify({"error": "Description is required"}), 400

    text = desc.lower()

    # Keyword overrides
    for rule in KEYWORD_NIC_OVERRIDES:
        if any(kw in text for kw in rule["keywords"]):
            return jsonify({"nic_code": rule["nic_code"]})

    # Similarity-based fallback
    if X_vec is not None:
        try:
            vec = vectorizer.transform([desc])
            sims = cosine_similarity(vec, X_vec)[0]
            best_idx = sims.argmax()
            return jsonify({"nic_code": nic_codes.iloc[best_idx]})
        except Exception as e:
            print(f"Prediction error: {e}")
            return jsonify({"error": "Prediction service unavailable"}), 500
    else:
        return jsonify({"error": "Model not loaded"}), 500

@app.route("/info")
def info_page():
    return render_template("info.html")

@app.route("/search")
def search_page():
    return render_template("search.html")

@app.route("/api/search/<code>")
def search_code(code):
    """API endpoint for searching NIC codes"""
    try:
        # Load the JSON data
        import json
        with open('finaldataset_yourgpt.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Build code index
        code_index = {}
        for item in data:
            if '__parsed_extra' in item and len(item['__parsed_extra']) > 2:
                nic_code = item['__parsed_extra'][1] or item['__parsed_extra'][0]
                description = item['__parsed_extra'][2]
                if nic_code and description:
                    code_index[nic_code] = description
                    print(f"Indexed: {nic_code} -> {description}")  # Debug print
        
        # Search for exact match
        result = code_index.get(code)
        if result:
            return jsonify({"code": code, "description": result})
        else:
            return jsonify({"error": "Code not found"}), 404
            
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({"error": "Search service unavailable"}), 500

@app.route("/finaldataset_yourgpt.json")
def serve_json():
    """Serve the JSON data file"""
    try:
        return send_from_directory('.', 'finaldataset_yourgpt.json')
    except Exception as e:
        print(f"Error serving JSON: {e}")
        return jsonify({"error": "Data file not available"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5002, host="0.0.0.0")