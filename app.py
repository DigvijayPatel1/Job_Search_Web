from flask import Flask, render_template
from db import load_data_from_db
from db import load_job_info
from flask import jsonify

app = Flask(__name__)



@app.route("/")
def home():
    jobs = load_data_from_db()
    return render_template("home.html", jobs = jobs)

@app.route("/job/<job_id>")
def profile(job_id):
    profile = load_job_info(job_id)
    if not profile:
        return "Not Found", 404
    return render_template("profile.html", job=profile)




if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)