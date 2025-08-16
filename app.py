from flask import Flask, render_template, request, url_for, redirect
from db import load_data_from_db, load_user_info, load_job_info
from flask import jsonify

app = Flask(__name__)


#route home page
@app.route("/")
def home():
    jobs = load_data_from_db()
    return render_template("home.html", jobs = jobs)

#route the job profile
@app.route("/job/<job_id>")
def profile(job_id):
    profile = load_job_info(job_id)
    if not profile:
        return "Not Found", 404
    return render_template("profile.html", job=profile)

#route the login page
@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Save into DB
        load_user_info({"email": email, "password": password})

        return redirect(url_for("home"))

    return render_template("login_form.html")




if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)