from flask import Flask, render_template, request, redirect, url_for
from generate_content import generate_course
from dotenv import load_dotenv
import markdown

load_dotenv()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/course', methods=['POST'])
def course():
    topic = request.form.get('topic')
    language = request.form.get('language')
    course_modules = generate_course(topic, language)
    modules = [markdown.markdown(module) for module in course_modules]
    # content = markdown.markdown(course_description)
    progress = 0  # Initial progress is 0%

    return render_template(
        'course.html',
        course_title=f"{topic} with {language}",
        modules=modules,
        progress=progress
    )


@app.route('/lesson/<int:lesson_id>')
def lesson(lesson_id):
    # Placeholder data for lessons
    lessons = [
        "Getting Started with Python",
        "Understanding Variables and Data Types",
        "Control Flow: If Statements and Loops",
        "Functions: Writing Reusable Code",
        "Working with Lists and Dictionaries",
    ]
    if 0 < lesson_id <= len(lessons):
        lesson_title = lessons[lesson_id - 1]
        return render_template('lesson.html', lesson_title=lesson_title, lesson_id=lesson_id)
    else:
        return "Lesson not found", 404


if __name__ == "__main__":
    app.run(debug=True)
