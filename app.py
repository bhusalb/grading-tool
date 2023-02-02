from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import ssh
import os
import canvas

load_dotenv()

app = Flask(__name__)

ssh_client = ssh.connect()

SERVER_WORKING_DIR = os.getenv('SERVER_WORKING_DIR')


@app.route('/')
def index():
    return render_template('select-lab.html')


@app.route('/make-backup', methods=['GET'])
def make_backup():
    args = request.args.to_dict()
    stdin, stdout, stderr = ssh_client.exec_command(f'{SERVER_WORKING_DIR}/backup.sh lab{args["lab_number"]}')

    output = stdout.read().decode('ASCII').replace('\n', '<br>')
    return render_template('backup.html', output=output, lab_number=args["lab_number"])


@app.route('/lab/<int:lab_id>/grading', methods=['GET'])
def grading(lab_id):
    my_submissions, my_students_dict, my_assignment = canvas.get_my_submissions_for_lab(lab_id)
    submissions = []

    for submission in my_submissions:
        submissions.append(
            {
                'pawprint': my_students_dict[submission.user_id].login_id,
                'name': my_students_dict[submission.user_id].name,
                'user_id': submission.user_id,
                'assignment_id': submission.assignment_id,
                'course_id': submission.course_id,
                'grade': submission.grade,
                'graded_at': submission.graded_at,
                'section': my_students_dict[submission.user_id].section,
                'id': submission.id,
            }
        )

    return render_template('grading.html', my_submissions=submissions, assignment_name=my_assignment.name,
                           lab_id=lab_id)


@app.route('/dev')
def dev():
    return render_template('dev.html', assignment_name='Lab DEV', lab_id=2)


@app.route('/lab/<int:lab>/code/<paw_print>', methods=['GET'])
def get_c_code_from_server(lab, paw_print):
    stdin, stdout, stderr = ssh_client.exec_command(f'cat {SERVER_WORKING_DIR}/cs1050_local_labs/lab{lab}_backup/{paw_print}/*')
    output = stdout.read().decode('ASCII')
    return jsonify(dict(output=output))


@app.route('/update-grade', methods=['POST'])
def update_grade():
    data = request.get_json()
    submission = canvas.update_grade(data)

    return jsonify({
        'grade': submission.grade,
        'comments': submission.submission_comments if hasattr(submission, 'submission_comments') else [],
        'graded_at': submission.graded_at
    })


if __name__ == '__main__':
    app.run()
