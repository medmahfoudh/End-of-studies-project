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
# candidates_collection = db['job_applicants']
job_collection = db['jobs']


@app.route('/' , methods = ["GET"])
def home():
    jobs_offers = mongo.db.jobs.find()
    return render_template('home.html' , jobs_offers=jobs_offers)

@app.route('/sign_in' , methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        admin = mongo.db.admins.find_one({"name": request.form["name"], "password": request.form["password"]})
        name_admin = request.form["name"]
        global_name_admin = name_admin
        jobs = mongo.db.jobs.find()
        global_jobs = jobs
        isAdmin = True
        if admin:
            session["admin"] = True
            isAdmin = True
            return render_template('/admin/dashboard.html' , name_admin=name_admin ,  jobs = jobs )
        else:
            isAdmin = False

            return render_template('sign_in.html' , isAdmin = isAdmin)
    return render_template('sign_in.html')




@app.route('/dashboard' , methods = ["GET"])
def dashboard():
    jobs = mongo.db.jobs.find()
    return render_template('/admin/dashboard.html' , jobs = jobs )
# @app.after_request
# def after_request(response):
#     response.headers["Cache-Control"] = "no-cahe, no-store,must-revalidate" 
#     return response

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/candidate_form/<job_id>' , methods=['GET', 'POST'])
def candidate_form(job_id):
    global global_job_id
    global_job_id = job_id
    job_id = mongo.db.jobs.find_one({"_id": ObjectId(job_id) })
    return render_template(('candidate_form.html') , job_id=job_id )
# ===============SUBMIT CANDIDAT ====================
@app.route('/candidate_form/submit', methods=['POST'])
def submit():
    global_job_id
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    cv = request.files['cv']
    cv_data = cv.read()

    # Save the data in MongoDB
    job_applicant = {
        "candidat_id":ObjectId(),
        "name": name,
        "email": email,
        "phone": phone,
        "cv": Binary(cv_data)
    }
    job_collection.update_one(
        {"_id": ObjectId(global_job_id)},
        {"$push": {"job_applicants": job_applicant}})
    return render_template('success_add_candidat.html')
    # return f"Job application submitted successfully!
# ===================FIN SUBMIT CANDIDT ==================
# =============DOWNLOAD CV===============
@app.route('/dashboard/classement/<id>' , methods=["GET"])
def classement(id): 
    candidates = mongo.db.jobs.find({"_id": ObjectId(id)})
    jn = candidates[0]['job_name']
    return render_template("/admin/classement.html", candidates=candidates , jn=jn)


@app.route("/dashboard/classement/<id>/cv", methods=["GET"])
def download_cv(id):
    unwound_job_applicants = list(mongo.db.jobs.aggregate([
    {"$unwind": "$job_applicants"},
    {"$match":{"job_applicants.candidat_id": ObjectId(id)}},
    {"$group":{"_id":"$job_applicants.cv"}}
    ]))
    cv_data = unwound_job_applicants[0]
    cv_data = cv_data['_id']
    response = make_response(cv_data)
    response.headers["Content-Disposition"] = f"attachment; filename={id}.pdf"
    return response
    # return f"test completed! {cv_data}  "

# ============AJOUTER LES OFFRES D'EMPLOI==================
@app.route("/dashboard/add_job" )
def jobs():
    return render_template('/admin/add_job.html')
@app.route("/add_job" , methods = ["POST"])
def add_job():
    job_name = request.form["job_name"]
    required_skills = request.form["required_skills"].split(',')
    job_description = request.form["job_description"]
    job_image = request.files["job_image"]

    if job_image:
        image_string = job_image.read()
        encoded_image = base64.b64encode(image_string).decode('utf-8')
    else:
        encoded_image = None


    job = {
        "job_name": job_name,
        "required_skills": required_skills,
        "job_description": job_description,
        "job_image": encoded_image
    }


    job_collection.insert_one(job)
    jobs = mongo.db.jobs.find()

    return render_template('/admin/dashboard.html' , jobs = jobs)

# ============FIN AJOUTER LES OFFRES D'EMPLOI==================
# ===============SUPPRIMER L'OFFRE D'EMPLOI====================
@app.route('/delete_job/<job_id>', methods=['POST','DELETE'])
def delete_job(job_id):
    mongo.db.jobs.delete_one({'_id': ObjectId(job_id)})
    jobs = mongo.db.jobs.find()

    return render_template('/admin/dashboard.html' , jobs = jobs )
# ===============FIN SUPPRIMER L'OFFRE D'EMPLOI====================

# =============AFTER REQUEST=============


# =============FIN AFTER REQUEST=============

if __name__ == '__main__':
    app.run(debug=True)