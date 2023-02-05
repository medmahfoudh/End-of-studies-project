from bson import ObjectId
from flask import Flask, make_response,render_template, request
from pymongo import MongoClient
from bson.binary import Binary


app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017")
db = client['SmartRecruiter']
candidates_collection = db['job_applicants']


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





# ===============SUBMIT CANDIDAT ====================
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    cv = request.files.get('cv')
    cv_data = cv.read()
    # Save the data in MongoDB
    applicant = {
        "name": name,
        "email": email,
        "phone": phone,
        "cv": Binary(cv_data)
    }
    candidates_collection.insert_one(applicant)
    # return "Job application submitted successfully!"
    return db.candidates_collection.find()

# ===================FIN SUBMIT CANDIDT ==================
# =============DOWNLOAD CV===============
@app.route('/dashboard/classement' , methods=["GET"])
def classement(): 
    candidates = db.candidates_collection.find()
    return render_template("/admin/classement.html", candidates=candidates)


@app.route("/dashboard/classement/<id>/cv", methods=["GET"])
def download_cv(id):
    candidate = db.candidates.find_one({"_id": ObjectId(id)})
    cv_data = candidate["cv"]
    response = make_response(cv_data)
    response.headers["Content-Disposition"] = "attachment; filename=cv.pdf"
    return response

@app.route("/candidates", methods=["GET"])
def view_candidates():
    candidateso = list(db.candidates_collection.find())
    return render_template("candidates.html", candidates=candidateso)


if __name__ == '__main__':
    app.run(debug=True)