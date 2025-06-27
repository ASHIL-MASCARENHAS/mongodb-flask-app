import certifi 
from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json
import datetime

load_dotenv()

app = Flask(__name__)

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "flask_db"
COLLECTION_NAME = "submissions"

@app.route('/api')
def api_data():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    print("Form data received:", request.form)
    try:
        client = MongoClient(
            MONGO_URI,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
            serverSelectionTimeoutMS=30000
        )
        
        # Force connection test
        client.admin.command('ping')
        
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        data = {
            "name": request.form['name'],
            "email": request.form['email'],
            "timestamp": datetime.datetime.now()
        }
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        
        return redirect(url_for('success'))
    except Exception as e:
        print("Full error:", str(e))
        return render_template('form.html', error="Database connection failed. Please try again later.")

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)