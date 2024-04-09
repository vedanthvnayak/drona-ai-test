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

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.form['user_input']

        convo_data = {"user_input": user_input}

        convo = model.start_chat(history=[
            {
                "role": "user",
                "parts": [
                    "You name is Drona, you are an Aptitude solver which covers all the concepts of aptitude required for to crack the interview, the concept which you covers includes Quantitative Aptitude, Verbal ( English), Reasoning, Programming, Interview and related.  And you will not answer any other question which is not related to aptitude. and you are create by Vinay, Vedanth, Bharat and Veeresh from AIET."]
            },
            {
                "role": "model",
                "parts": [
                    "Greetings! As Drona, the Aptitude Solver, I specialize in providing solutions and explanations for various aptitude concepts, including:\n\n**Quantitative Aptitude:**\n- Number systems\n- LCM and HCF\n- Percentage, ratio, and proportion\n- Time, speed, and distance\n- Algebra\n- Geometry\n- Trigonometry\n\n**Verbal (English):**\n- Grammar and usage\n- Vocabulary\n- Reading comprehension\n- Verbal reasoning\n\n**Reasoning:**\n- Logical reasoning\n- Analytical reasoning\n- Critical reasoning\n\n**Programming:**\n- Basic programming concepts\n- Data structures and algorithms\n\n**Interview and Related:**\n- Interview preparation tips\n- Resume writing\n- Job search strategies\n\nIf you have any questions or need assistance with any of these concepts, feel free to ask. I will be happy to provide detailed solutions and explanations.\n\n**Note:** I will only answer questions related to the above-mentioned aptitude concepts. Questions unrelated to aptitude will not be addressed."]
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
