# IEOR Course Recommendation and Planning System

The Course Recommendation and Planning System is a web-based prototype designed for undergraduate students in Columbia University's Department of Industrial Engineering and 
Operations Research (IEOR), with a focus on those pursuing the Financial Engineering track. This prototype, built using Flask, simulates a functional academic planning tool where students 
can create accounts, edit their academic profiles, view dynamically generated course recommendations, and plan out their academic trajectory over eight semesters. Students begin by 
registering and logging into the system. Once logged in, they are directed to a profile page where they can edit key details such as their name, UNI, major, and current academic semester. 
The system represents academic progress using a “Semester #” format (e.g., Semester 5 for Junior Fall), and automatically adjusts how many past semesters are shown based on that selection.
A placeholder image is used for student ID photos, with future plans for automated imports based on UNI.

The platform also includes a course history page, which presents past coursework organized by semester in collapsible dropdowns. Each section is dynamically generated based on how many 
semesters a student has completed. The course recommendation page allows students to select any upcoming semester from a dropdown and choose whether or not to include electives in their 
suggestions. The resulting recommendations update accordingly and reflect a mixture of required and elective coursework modeled on the Financial Engineering degree requirements. Finally, 
the semester planning interface allows students to view their full academic plan from Semesters 1 through 8. Each semester is labeled by year and term (e.g., Sophomore Spring, Senior Fall) 
and expands to reveal a list of courses. While currently using hardcoded dummy data, the structure is built to support future integration with real student records, advising tools, and 
institutional APIs.

All HTML templates are modular and extend from a shared base layout, and the system includes a working session-based login flow. While this project currently functions as a front-end 
prototype, it is structured to scale into a complete, data-driven advising platform in future iterations.

## Project Structure
<pre><code> course-recommendation/ ├── app.py # Flask application ├── schema.sql # Database schema (for future use) ├── courses.db # Placeholder SQLite database ├── requirements.txt # Python dependencies ├── static/ │ └── placeholder-id.png # Default ID photo └── templates/ ├── base.html ├── login.html ├── register.html ├── dashboard.html ├── profile.html ├── recommendations.html ├── course_history.html └── plan.html </code></pre>

## How to Run Locally

```bash
git clone https://github.com/Columbia-IEOR/course-recommendation.git
cd course-recommendation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py
flask run
```
Then visit: http://127.0.0.1:5000

-----------------
This version:
- Is one continuous markdown file
- Has clean indentation and tree formatting
- Will render perfectly on GitHub without visual glitches
