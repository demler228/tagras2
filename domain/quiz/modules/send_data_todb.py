import psycopg2 # type: ignore
import json

def send_to_db(quiz_data, theme_name):

    conn = psycopg2.connect(
        dbname="test_qwiz",
        user="postgres",
        password="nejmard16",
        host="127.0.0.1",
        port="5432"
    )
    cur = conn.cursor()

    cur.execute("INSERT INTO themes (theme_name) VALUES (%s) RETURNING id", (theme_name,))
    theme_id = cur.fetchone()[0]

    for question_data in quiz_data:
        cur.execute(
            "INSERT INTO questions (theme_id, question_text) VALUES (%s, %s) RETURNING id",
            (theme_id, question_data["question"])
        )
        question_id = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO answers (question_id, answer_text, is_correct) VALUES (%s, %s, %s)",
            (question_id, question_data["correct_answer"], True)
        )

        for incorrect_answer in question_data["incorrect_answers"]:
            cur.execute(
                "INSERT INTO answers (question_id, answer_text, is_correct) VALUES (%s, %s, %s)",
                (question_id, incorrect_answer, False)
            )

    conn.commit()
    cur.close()
    conn.close()