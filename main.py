import base64
from bson import ObjectId
from flask import Flask, make_response, redirect,render_template, request, session, url_for 
from pymongo import MongoClient 
from flask_pymongo import PyMongo
from bson.binary import Binary 



app = Flask(__name__)
app.secret_key = " "
client = MongoClient("mongodb://localhost:27017/SmartRecruiter")
app.config["MONGO_URI"] = "mongodb://localhost:27017/SmartRecruiter"
mongo = PyMongo(app)
db = client['SmartRecruiter']
candidates_collection = db['job_applicants']
job_collection = db['jobs']


@app.route('/' , methods = ["GET"])
def home():
    jobs_offers = mongo.db.jobs.find()
    return render_template('home.html' , jobs_offers=jobs_offers)

@app.route('/sign_in' , methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        admin = mongo.db.admins.find_one({"name": request.form["name"], "password": request.form["password"]}) 
        if admin:
            session["admin"] = True
            return redirect(url_for("dashboard") )
        else:
            return redirect(url_for("sign_in"))
    return render_template('sign_in.html')

# @app.route("/protected_resource")
# def protected_resource():
#     if "admin" in session:
#         return render_template('/admin/dashboard.html' )
#     else:
#         return redirect(url_for("sign_in"))


@app.route('/dashboard' , methods = ["GET"])
def dashboard():
    jobs = mongo.db.jobs.find()
    return render_template('/admin/dashboard.html' , jobs = jobs )

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/candidate_form/<job_id>' , methods=['GET', 'POST'])
def candidate_form(job_id):
    job_id = mongo.db.jobs.find_one({"_id": ObjectId(job_id) })
    return render_template(('candidate_form.html') , job_id=job_id)

@app.route('/candidate_form/<job_id>/submit' , methods=['POST'])
def add_candidate():
    job_id = request.form.get("job_id")
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    cv = request.files.get('cv')
    cv_data = cv.read()
 
    job = mongo.db.jobs.find_one({"_id": ObjectId(job_id)})
    # Save the data in MongoDB
    applicant = {
        "name": name,
        "email": email,
        "phone": phone,
        "cv": Binary(cv_data)
    }
    mongo.db.jobs.update_one(
        {"_id": ObjectId(job_id)},
        {"$push": {"Job_applicants": applicant}}
    )
    return "Candidate added successfully"


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
    return "Job application submitted successfully!"

# ===================FIN SUBMIT CANDIDT ==================
# =============DOWNLOAD CV===============
@app.route('/dashboard/classement' , methods=["GET"])
def classement(): 
    candidates = mongo.db.job_applicants.find()
    return render_template("/admin/classement.html", candidates=candidates)


@app.route("/dashboard/classement/<id>/cv", methods=["GET"])
def download_cv(id):
    candidate = mongo.db.job_applicants.find_one({"_id": ObjectId(id)})
    cv_data = candidate["cv"]
    response = make_response(cv_data)
    response.headers["Content-Disposition"] = "attachment; filename=cv.pdf"
    return response

# ============AJOUTER LES OFFRES D'EMPLOI==================
@app.route("/dashboard/add_job" )
def jobs():
    return render_template('/admin/add_job.html')
@app.route("/add_job" , methods = ["POST"])
def add_job():
    job_name = request.form["job_name"]
    required_skills = request.form["required_skills"].split()
    job_description = request.form["job_description"]
    job_image = request.files["job_image"]
    
    if job_image:
        image_string = job_image.read()
        encoded_image = base64.b64encode(image_string).decode('utf-8')
    else:
        encoded_image = None

    # Create a new job document
    job = {
        "job_name": job_name,
        "required_skills": required_skills,
        "job_description": job_description,
        "job_image": encoded_image
    }

    # Insert the job document into the collection
    job_collection.insert_one(job)
    return "<h1>Job Added!</h1>"
# redirect("/dashboard")

# ============FIN AJOUTER LES OFFRES D'EMPLOI==================

if __name__ == '__main__':
    app.run(debug=True)