from flask import Flask,render_template
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017")
db = client['SmartRecruiter']
collection = db['job_applicant']


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/dashboard')
def dashboard():
    return render_template('/admin/dashboard.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/candidate_form')
def candidate_form():
    return render_template('candidate_form.html')

@app.route('/dashboard/id/classement')
def classement(): 
    return render_template('/admin/classement.html')

if __name__ == '__main__':
    app.run(debug=True)