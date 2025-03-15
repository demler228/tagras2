def remove_empty_lines(text):
    return "\n".join(line for line in text.splitlines() if line.strip())

def add_incorrect_answers(quiz_data):
    for question_data in quiz_data:
        correct_answer = question_data["correct_answer"]
        all_answers = question_data["answers"]

        incorrect_answers = [answer for answer in all_answers if answer != correct_answer]

        question_data["incorrect_answers"] = incorrect_answers

    return quiz_data