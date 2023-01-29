from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sing_in')
def sign_in():
    return render_template('auth.html')

if __name__ == '__main__':
    app.run(debug=True)