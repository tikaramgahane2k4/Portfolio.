import os
from flask import Flask, render_template, request, redirect, url_for, flash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, 'frontend'))

app = Flask(
    __name__,
    template_folder=os.path.join(FRONTEND_DIR, 'templates'),
    static_folder=os.path.join(FRONTEND_DIR, 'static'),
    static_url_path='/static'
)

# Simple .env loader
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    print(f"--- LOADING {env_path} ---")
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                os.environ[key] = value
                print(f"Loaded: {key}")
else:
    print(f"--- WARNING: {env_path} NOT FOUND ---")

app.secret_key = os.urandom(24)  # Required for flash messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/contact', methods=['POST'])
def contact():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not name or not email or not message:
            flash("All fields are required!", "error")
            return redirect(url_for('index') + '#contact')

        # Message received acknowledgment
        flash("Message received! Thank you for reaching out.", "success")
        print(f"--- MESSAGE RECEIVED ---")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Message: {message}")
        
    except Exception as e:
        print(f"--- ERROR ---")
        print(f"Error details: {e}")
        flash("An error occurred. Please try again.", "error")
    
    return redirect(url_for('index') + '#contact')

if __name__ == '__main__':
    # For development use Flask's built-in server
    app.run(debug=True, port=5000)

# For production, use Gunicorn:
#   gunicorn -w 4 -b 0.0.0.0:5000 app:app
# This will serve static files more efficiently and handle more requests smoothly.
