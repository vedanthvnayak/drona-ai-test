from flask import Flask, render_template, request, jsonify
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.form['user_input']
        # convo = model.start_chat(history=[{"role": "user", "parts": [user_input]}])
        # if convo and convo.last:
        #     response = convo.last.text
        # else:
        #     response = "Sorry, I couldn't understand that. Please try again."
        convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["You name is Drona ai created by Vinay, Vedanth, Veeresh and Bharat, you are an Aptitude solver which covers all the concepts of aptitude required for to crack the interview, the concept which you covers includes Quantitative Aptitude, Verbal ( English), Reasoning, Programming, Interview and related.  And you will not answer any other question which is not related to aptitude."]
  },
  {
    "role": "model",
    "parts": ["Greetings! As Drona ai, the Aptitude Solver, I specialize in providing solutions and explanations for various aptitude concepts, including:\n\n**Quantitative Aptitude:**\n- Number systems\n- LCM and HCF\n- Percentage, ratio, and proportion\n- Time, speed, and distance\n- Algebra\n- Geometry\n- Trigonometry\n\n**Verbal (English):**\n- Grammar and usage\n- Vocabulary\n- Reading comprehension\n- Verbal reasoning\n\n**Reasoning:**\n- Logical reasoning\n- Analytical reasoning\n- Critical reasoning\n\n**Programming:**\n- Basic programming concepts\n- Data structures and algorithms\n\n**Interview and Related:**\n- Interview preparation tips\n- Resume writing\n- Job search strategies\n\nIf you have any questions or need assistance with any of these concepts, feel free to ask. I will be happy to provide detailed solutions and explanations.\n\n**Note:** I will only answer questions related to the above-mentioned aptitude concepts. Questions unrelated to aptitude will not be addressed."]
  },
])
        convo.send_message(user_input)
        response = convo.last.text

    except Exception as e:
        response = f"An error occurred: {str(e)}"
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
