from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/candidate_form')
def candidate_form():
    return render_template('candidate_form.html')

if __name__ == '__main__':
    app.run(debug=True)