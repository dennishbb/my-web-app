from flask import Flask, render_template, request, send_file
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from fuzzywuzzy import fuzz
import os

app = Flask(__name__, template_folder="templates")
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    processed_path = process_data(file_path, file.filename)
    return send_file(processed_path, as_attachment=True)


def process_data(file_path, filename):
    df = pd.read_csv(file_path)
    
    # Detect Missing Values
    df.fillna("MISSING", inplace=True)
    
    # Identify Duplicates
    df.drop_duplicates(inplace=True)
    
    # Anomaly Detection
    if not df.select_dtypes(include=[np.number]).empty:
        iso_forest = IsolationForest(contamination=0.05, random_state=42)
        df['Anomaly_Score'] = iso_forest.fit_predict(df.select_dtypes(include=[np.number]))
        df = df[df['Anomaly_Score'] != -1]  # Remove detected anomalies
    
    # Fuzzy Matching Example (if 'Name' column exists)
    if 'Name' in df.columns:
        df['Name'] = df['Name'].astype(str)
        df['Name_Cleaned'] = df['Name'].apply(lambda x: x.title())
    
    processed_file_path = os.path.join(PROCESSED_FOLDER, f"cleaned_{filename}")
    df.to_csv(processed_file_path, index=False)
    return processed_file_path

if __name__ == '__main__':
    app.run(debug=True)

