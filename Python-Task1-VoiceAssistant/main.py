from flask import Flask, render_template, jsonify, request
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process-command', methods=['POST'])
def process_command():
    data = request.get_json()
    user_query = data.get('query', '').lower()
    
    response_text = ""
    action_type = "speak"
    action_data = ""

    if 'time' in user_query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        response_text = f"The current time is {current_time}"
    
    elif 'date' in user_query:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        response_text = f"Today's date is {current_date}"
        
    elif 'open google' in user_query:
        response_text = "Opening Google for you."
        action_type = "open_url"
        action_data = "https://www.google.com"
        
    elif 'open youtube' in user_query:
        response_text = "Opening YouTube."
        action_type = "open_url"
        action_data = "https://www.youtube.com"
        
    elif 'hello' in user_query or 'hi' in user_query:
        response_text = "Hello Anjali! How can I help you with your internship project today?"
        
    else:
        response_text = f"Searching the web for {user_query}"
        action_type = "open_url"
        action_data = f"https://www.google.com/search?q={user_query}"

    return jsonify({
        "response": response_text,
        "action": action_type,
        "data": action_data
    })

if __name__ == '__main__':
    app.run(debug=True)