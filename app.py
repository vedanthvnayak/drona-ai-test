from flask import Flask, render_template, request, jsonify
import json
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="AIzaSyCca-hZMI6_QmGkzEC1kqPJreFEkX03A9g")

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro", generation_config=generation_config, safety_settings=safety_settings
)

# List to store conversation data
conversation_data = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.form['user_input']

        convo_data = {"user_input": user_input}

        convo = model.start_chat(history=[
            {
                "role": "user",
                "parts": [user_input]
            },
            {
                "role": "model",
                "parts": ["Greetings!..."]
            },
        ])

        convo.send_message(user_input)
        response = convo.last.text

        # Save the conversation data
        convo_data["response"] = response
        conversation_data.append(convo_data)

        # Save conversation data to a JSON file
        with open('conversation_data.json', 'w') as json_file:
            json.dump(conversation_data, json_file, indent=4)

    except Exception as e:
        response = f"An error occurred: {str(e)}"

    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)
