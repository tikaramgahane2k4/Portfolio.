import os
from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

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

        # EMAIL CONFIGURATION
        # This is where the message will be delivered
        receiver_email = "pawangahane02@gmail.com"
        
        # This is the account used to authenticate with Google
        # If not set in .env, we assume it's the same as receiver_email
        sender_email = os.environ.get('MAIL_SENDER', receiver_email)
        sender_password = os.environ.get('MAIL_PASSWORD')
        if sender_password:
            sender_password = sender_password.replace(" ", "")

        if not sender_password:
            print("--- SMTP ERROR: MAIL_PASSWORD is not set in .env file ---")
            flash("Server configuration error: MAIL_PASSWORD not set.", "error")
            return redirect(url_for('index') + '#contact')

        print(f"--- ATTEMPTING EMAIL SEND ---")
        # Masking for privacy but showing first/last chars for verification
        masked_pass = sender_password[0] + "****" + sender_password[-1] if len(sender_password) > 2 else "****"
        print(f"Sender (Login User): {sender_email}")
        print(f"Receiver (Delivery): {receiver_email}")
        print(f"Password Verify: {masked_pass} (Length: {len(sender_password)})")

        # Create message
        msg = MIMEMultipart()
        msg['Subject'] = f"New Portfolio Message from {name}"
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg.add_header('reply-to', email)

        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        msg.attach(MIMEText(body, 'plain'))

        # SMTP Server setup
        print("Connecting to smtp.gmail.com:587...")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.set_debuglevel(1) # This will show the actual conversation in terminal
            server.starttls()
            print(f"Authenticating as {sender_email}...")
            server.login(sender_email, sender_password)
            print("Authentication successful! Sending message...")
            server.send_message(msg)
            print("Message sent successfully!")

        flash("Message Sent Successfully!", "success")
    except smtplib.SMTPAuthenticationError as e:
        print("--- SMTP AUTHENTICATION FAILED ---")
        print(f"Error Code: {e.smtp_code}")
        print(f"Error Message: {e.smtp_error.decode() if isinstance(e.smtp_error, bytes) else e.smtp_error}")
        print("Reason: Google rejected your credentials. Check if your App Password is correct for the sender email.")
        flash("Login failed. Please check your App Password.", "error")
    except smtplib.SMTPConnectError:
        print("--- SMTP CONNECTION FAILED ---")
        print("Reason: Could not connect to smtp.gmail.com. Check your internet connection.")
        flash("Could not connect to the mail server.", "error")
    except Exception as e:
        print(f"--- SMTP GENERAL ERROR ---")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {e}")
        flash(f"Failed to send message.", "error")
    
    return redirect(url_for('index') + '#contact')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
