from flask import Flask, request, session, redirect, render_template, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import json
import os
from demo_data import demo_users
from functools import wraps
from flask import session, redirect


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_uni" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)
app.secret_key = "dev"  # For development only

# --------------------------
# Database Connection Helper
# --------------------------
def get_db():
    conn = sqlite3.connect('courses.db')
    conn.row_factory = sqlite3.Row
    return conn

# --------------------------
# Homepage Route
# --------------------------
@app.route('/')
def index():
    if "user_id" in session:
        return redirect("/dashboard")
    return redirect("/login")

# --------------------------
# Registration Route
# --------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uni = request.form["uni"]
        name = request.form["name"]
        password = request.form["password"]  # unused, placeholder

        if uni not in demo_users:
            return "This UNI is not preloaded in demo_data.py. Please use ar4334 or yk4567."

        # Update name from form input (optional, or leave original)
        demo_users[uni]["name"] = name
        session["user_uni"] = uni
        return redirect("/dashboard")

    return render_template("register.html")

# --------------------------
# Login Route
# --------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uni = request.form["uni"]
        if uni in demo_users:
            session["user_uni"] = uni
            return redirect("/dashboard")
        return "Invalid UNI"
    return render_template("login.html")

# --------------------------
# Logout Route
# --------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# --------------------------
# Dashboard Route
# --------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    uni = session.get("user_uni")
    if not uni or uni not in demo_users:
        return redirect("/login")
    user = demo_users[uni]
    return render_template("dashboard.html", user=user)

# --------------------------
# API Endpoint to View All Courses (JSON)
# --------------------------
@app.route('/api/courses')
def api_courses():
    db = get_db()
    rows = db.execute("SELECT * FROM courses").fetchall()
    return jsonify([dict(row) for row in rows])

@app.route("/profile", methods=["GET", "POST"])
def profile():
    # Dummy hardcoded user (you'll replace this with DB later)
    default_user = {
        "name": "Afsana Rahman",
        "uni": "ar1234",
        "major": "Financial Engineering",
        "semester": 5  # e.g., Junior Fall = Semester 5
    }

    if request.method == "POST":
        # In a real app, you'd save these to a database
        default_user["name"] = request.form["name"]
        default_user["uni"] = request.form["uni"]
        default_user["major"] = request.form["major"]
        default_user["semester"] = int(request.form["semester"])

    # Calculate how many past semesters exist
    semesters_completed = default_user["semester"] - 1

    return render_template("profile.html", user=default_user, semesters_completed=semesters_completed)

@app.route("/courses")
@login_required
def all_courses():
    import re
    data_path = os.path.join("data", "2025-Fall.json")

    with open(data_path, "r") as f:
        raw_courses = json.load(f)

    tag_keywords = {
        "IEOR Core": ["IEOR E3608", "IEOR E4000", "Stochastic", "Simulation", "Optimization", "Financial Engineering"],
        "Programming": ["Python", "Java", "Programming", "Data Structures"],
        "Quantitative": ["Probability", "Statistics", "Regression"],
        "CS Elective": ["COMS", "CSOR", "COMS W3134"],
        "Technical Elective": ["Machine Learning", "Data Science", "Big Data", "Algorithms"],
        "Management Elective": ["Management", "Strategy", "Operations"]
    }

    # Build simplified course data with tags
    courses = []
    for course in raw_courses:
        title = course.get("course_title", "")
        department = course.get("department_name", "")
        instructor = course.get("instructor_name", "")
        code = course.get("course_code", "")
        tags = []

        for tag, keywords in tag_keywords.items():
            for kw in keywords:
                if kw.lower() in title.lower() or kw.lower() in code.lower():
                    tags.append(tag)
                    break

        courses.append({
            "code": code,
            "title": title,
            "department": department,
            "instructor": instructor,
            "tags": tags
        })

    # Get search query + tag filter
    query = request.args.get("q", "").strip().lower()
    selected_tag = request.args.get("tag", "").strip()

    # Apply search filter
    if query:
        courses = [
            c for c in courses
            if query in c["title"].lower()
            or query in c["code"].lower()
            or query in c["department"].lower()
            or query in c["instructor"].lower()
        ]

    # Apply tag filter
    if selected_tag:
        courses = [c for c in courses if selected_tag in  c["tags"]]


    return render_template("courses.html", courses=courses, query=query, selected_tag=selected_tag)


@app.route("/plan")
@login_required
def plan():
    semester_plan = {
        1: ["MATH UN1101 – Calculus I", "UW Writing", "IEOR E2261 – Intro to OR"],
        2: ["MATH UN1102 – Calculus II", "CS1004 – Python", "IEOR E3106 – Prob Models"],
        3: ["STAT GU4001 – Prob & Stats", "IEOR E4307 – Financial Engineering"],
        4: ["IEOR E4501 – Big Data", "ECON UN3412 – Econometrics"],
        5: ["IEOR E4106 – Stochastic Models", "COMS W3134 – Data Structures"],
        6: ["IEOR E4404 – Optimization Models", "IEOR E4701 – Machine Learning"],
        7: ["IEOR E4650 – Deep Learning", "IEOR E4999 – Senior Seminar"],
        8: ["IEOR E4570 – Systems Engineering", "IEOR E4999 – Capstone"]
    }

    return render_template("plan.html", plan=semester_plan)
       
@app.route("/course-history")
@login_required
def course_history():
    # Get number of semesters from query parameter (sent by profile page)
    semesters_completed = int(request.args.get("semesters", 1))

    # Dummy course map for now
    dummy_courses = {
        1: ["MATH UN1101 – Calculus I", "UW Writing", "IEOR E2261 – Intro to OR"],
        2: ["MATH UN1102 – Calculus II", "IEOR E3106 – Prob Models", "CS1004 – Python"],
        3: ["STAT GU4001 – Prob & Stats", "IEOR E4407 – Simulation"],
        4: ["IEOR E4501 – Big Data", "ECON UN3412 – Econometrics"],
        5: ["IEOR E4307 – Financial Engineering", "IEOR E4106 – Stochastic Models"]
    }

    # Compile course history for completed semesters
    course_history = []
    for semester in range(1, semesters_completed + 1):
        course_history.append({
            "number": semester,
            "label": f"Semester {semester}",
            "courses": dummy_courses.get(semester, ["No data for this semester"])
        })

    return render_template("course_history.html", history=course_history)

@app.route("/recommendations")
@login_required
def recommendations():
    semester = int(request.args.get("semester", 5))  # default to Semester 5
    include_electives = request.args.get("electives") == "on"

    # Dummy recommended courses by semester
    core_recommendations = {
        5: ["IEOR E4307 – Financial Engineering", "IEOR E4106 – Stochastic Models", "COMS W3134 – Data Structures"],
        6: ["IEOR E4404 – Optimization Models", "IEOR E4701 – Machine Learning for OR"],
        7: ["IEOR E4999 – Senior Seminar", "IEOR E4650 – Deep Learning"],
        8: ["IEOR E4999 – Capstone", "IEOR E4570 – Systems Engineering"]
    }

    elective_suggestions = {
        5: ["ECON UN3412 – Intro to Econometrics"],
        6: ["STAT GU4203 – Applied Regression"],
        7: ["IEOR E4407 – Simulation (Elective)"],
        8: ["CSOR W4246 – Algorithms for Data Science"]
    }

    # Build response
    recommended_courses = core_recommendations.get(semester, [])
    if include_electives:
        recommended_courses += elective_suggestions.get(semester, [])

    return render_template("recommendations.html",
                           selected_semester=semester,
                           include_electives=include_electives,
                           recommended_courses=recommended_courses)
