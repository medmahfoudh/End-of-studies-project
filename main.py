from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'This is My First App in Flask!'

if __name__ == '__main__':
    app.run(debug=True)