from flask import Flask, request, session, redirect, render_template, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'dev'  # For development only

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
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = get_db()
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        try:
            db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password))
            db.commit()
            return redirect('/login')
        except:
            return "User already exists. Try a different username."

    return render_template('register.html')

# --------------------------
# Login Route
# --------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = get_db()
        username = request.form['username']
        password = request.form['password']

        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            return redirect('/dashboard')
        return "Invalid username or password."

    return render_template('login.html')

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
@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect('/login')

    db = get_db()
    courses = db.execute("SELECT * FROM courses").fetchall()
    return render_template("dashboard.html", courses=courses)

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
def courses():
    return render_template("courses.html")

@app.route("/plan")
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


