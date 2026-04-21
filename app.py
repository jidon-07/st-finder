import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# 1. Setup API Key (Get yours from aistudio.google.com)
API_KEY = "AIzaSyB7BY-vU480heB0HBX_Hyovg3RGfMrCGDM"
genai.configure(api_key=API_KEY)

# 2. Use the latest stable model as of April 2026
# 'gemini-2.5-flash' provides the best balance of speed and accuracy
model = genai.GenerativeModel('gemini-2.5-flash')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        news_text = data.get('text', '')

        if not news_text.strip():
            return jsonify({'result': 'Error: Please enter text'})

        # Professional prompt for real-time analysis
        prompt = f"""
        Act as a professional fact-checker. Analyze this news content using real-time world data:
        "{news_text}"
        
        Respond with ONLY the word 'REAL' or 'FAKE'. 
        If unsure, provide the most likely classification based on current sources.
        """
        
        response = model.generate_content(prompt)
        # Clean the response to ensure it matches the UI CSS classes
        final_result = response.text.strip().upper()

        if "REAL" in final_result:
            status = "REAL"
        elif "FAKE" in final_result:
            status = "FAKE"
        else:
            status = "UNCERTAIN"

        return jsonify({'result': status})

    except Exception as e:
        # Returns the error to the UI for easier debugging
        return jsonify({'result': f"System Error: {str(e)}"})

if __name__ == '__main__':
    # Running on port 5000 is standard for Flask
    app.run(debug=True, port=5000)