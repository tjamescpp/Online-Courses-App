from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import markdown

try:
    from .generate_content import generate_course, generate_more_info
except ImportError:
    from generate_content import generate_course, generate_more_info

load_dotenv()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/course', methods=['POST'])
def course():
    topic = request.form.get('topic')
    language = request.form.get('language')
    modules = generate_course(topic, language)
    modules = [markdown.markdown(module) for module in modules]
    # content = markdown.markdown(course_description)
    progress = 0  # Initial progress is 0%

    return render_template(
        'course.html',
        course_title=f"{topic} with {language}",
        modules=modules,
        progress=progress
    )


@app.route('/module-details', methods=['POST'])
def module_details():
    module_name = request.form.get('module')

    if not module_name:
        return "Error: No module provided", 400

    # Generate details for the module using OpenAI
    generated_content = generate_more_info(module_name)
    print(generated_content)
    generated_content = markdown.markdown(generated_content, extensions=[
                                          'fenced_code', 'codehilite'])

    # Render the details page with the generated content
    return render_template('module_details.html', content=generated_content)


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
