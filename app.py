from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

DATA_FILE = "students.json"

# Create file if not exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def load_students():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_students(students):
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=4)

@app.route("/")
def home():
    students = load_students()
    return render_template("home.html", students=students)

@app.route("/add", methods=["POST"])
def add_student():
    student_id = request.form.get("id")
    name = request.form.get("name")
    course = request.form.get("course")

    students = load_students()

    new_student = {
    "id": int(student_id) ,
    "name": name,
    "course": course
    }

    students.append(new_student)
    save_students(students)

    return redirect(url_for("home"))

@app.route("/delete/<int:student_id>")
def delete_student(student_id):
    students = load_students()
    students = [s for s in students if s["id"] != student_id]
    save_students(students)
    return redirect(url_for("home"))

# Health check for CI/CD
@app.route("/health")
def health():
    return jsonify({"status": "OK"})

@app.route("/edit/<int:student_id>")
def edit_student(student_id):
    students = load_students()
    student = next((s for s in students if s["id"] == student_id), None)
    return render_template("edit.html", student=student)


@app.route("/update/<int:student_id>", methods=["POST"])
def update_student(student_id):
    students = load_students()

    for student in students:
        if student["id"] == student_id:
            student["name"] = request.form.get("name")
            student["course"] = request.form.get("course")

    save_students(students)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)