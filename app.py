import os
from flask import Flask, render_template, request, jsonify

from openai import OpenAI
from typing import Any, Dict
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address



client = OpenAI()
 
app = Flask(__name__)
app = Flask(__name__, template_folder='templates')

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["1000 per day", "1000 per hour"],
    storage_uri="memory://",
)  

@app.route('/generate-colors', methods=['POST'])
@limiter.limit("1000 per day", error_message='Rate limit exceeded. Please try again later.')
def generate_colors():
    data = request.get_json(silent=True)
    if data and 'query' in data:
        user_query = data['query']
    else:
        user_query = 'random colors'
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format={ "type": "json_object" },
            messages=[
                    {"role": "system", "content": "You are a hex color generator which genrates html color codes based on input. Total output colors should be in range of 2 to 8 in json format"},
                    {"role": "user", "content": "green trees"},
                    {"role": "assistant", "content": " colors:[\"#FCFCFC\",\"#EE1616\",\"#A50F0F\",\"#822222\",\"#815252\"]"},
                    {"role": "user", "content": "sky"},
                    {"role": "assistant", "content": "colors:[\"#1BE1CC\",\"#2BB8A9\",\"#319F93\",\"#2494AF\",\"#72C4D8\"]"},

                    {"role": "user", "content": "color pallete of"+user_query},
            ]
        )
        generated_content = response.choices[0].message.content
        return generated_content
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    

   

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)

 
@app.route('/')
def home():
    return render_template('index.html')


