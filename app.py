from flask import Flask, render_template, request, url_for, redirect, session
from db import load_data_from_db, load_user_info, load_job_info
from flask import jsonify
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret") #added secret key

#route home page
@app.route("/")
def home():
    jobs = load_data_from_db()
    user_email = session.get("user_email")
    return render_template("home.html", jobs = jobs)

#route the job profile
@app.route("/job/<job_id>")
def profile(job_id):
    profile = load_job_info(job_id)
    if not profile:
        return "Not Found", 404
    user_email = session.get("user_email")
    return render_template("profile.html", job=profile)

#route the login page
@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Save into DB
        load_user_info({"email": email, "password": password})

        #store login state
        session["user_email"] = email

        return redirect(url_for("home"))

    return render_template("login_form.html")

@app.route("/logout")
def logout():
    session.pop("user_name", None)
    return redirect(url_for("home"))




if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)