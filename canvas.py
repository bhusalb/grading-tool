from canvasapi import Canvas
import os


def get_canvas():
    return Canvas(os.getenv('CANVAS_API_URL'), os.getenv('CANVAS_API_KEY'))


def get_my_submissions_for_lab(lab_number):
    canvas = get_canvas()
    course = canvas.get_course(os.getenv('CANVAS_COURSE_ID'))
    my_assignment = None
    for assignment in course.get_assignments():
        lower_case = assignment.name.lower()
        if 'pre' not in lower_case and f'lab {lab_number}' in lower_case:
            my_assignment = assignment
            break
    groups = course.get_groups()
    my_group = None
    for group in groups:
        if group.name == os.getenv('CANVAS_GRADER_NAME'):
            my_group = group
            break

    my_submissions = []
    if my_assignment and my_group:
        submissions = my_assignment.get_submissions()
        my_students_dict = dict()
        for user in my_group.get_users():
            my_students_dict[user.id] = user

        for submission in submissions:
            if submission.user_id in my_students_dict:
                my_submissions.append(submission)

    return my_submissions, my_students_dict, my_assignment


def update_grade(data):
    canvas = get_canvas()
    course = canvas.get_course(os.getenv('CANVAS_COURSE_ID'))
    assignment = course.get_assignment(data['assignment_id'])
    submission = assignment.get_submission(data['user_id'])

    updated_fields = dict()
    if 'new_grade' in data:
        updated_fields['submission'] = dict(posted_grade=data['new_grade'])

    if 'new_comment' in data:
        updated_fields['comment'] = dict(text_comment=data['new_comment'])

    if updated_fields:
        submission.edit(
            **updated_fields
        )

    return submission
