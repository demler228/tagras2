import os
import json
import sys
import whisper
import requests
import uuid
from pdfminer.high_level import extract_text
import moviepy as mp
import re

client_id = "ce7d7680-4bf7-4ff3-b172-3be3794aa5b8"
secret = "338c3cfd-1038-4d2b-9e27-5af3a3d7f728"
auth = "Y2U3ZDc2ODAtNGJmNy00ZmYzLWIxNzItM2JlMzc5NGFhNWI4OjMzOGMzY2ZkLTEwMzgtNGQyYi05ZTI3LTVhZjNhM2Q3ZjcyOA=="


def remove_empty_lines(text):
    return "\n".join(line for line in text.splitlines() if line.strip())


def process_pdf(pdf_path):
    text = extract_text(pdf_path)
    return remove_empty_lines(text)


def process_video(video_path, audio_path="audio_temp.mp3"):
    clip = mp.VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, codec="mp3")

    model = whisper.load_model("base")
    result = model.transcribe(audio_path, fp16=False)

    os.remove(audio_path)
    return result["text"]


def get_token(scope="GIGACHAT_API_PERS"):
    rq_uid = str(uuid.uuid4())
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": rq_uid,
        "Authorization": f"Basic {auth}",
    }
    payload = {"scope": scope}
    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response.json().get("access_token", None)
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return None


def get_quiz_questions(auth_token, text):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    payload = json.dumps(
        {
            "model": "GigaChat",
            "messages": [
                {
                    "role": "user",
                    "content": f"""
Сгенерируй 10 вопросов по тексту: {text}. Каждый вопрос должен быть в следующем формате:
Вопрос
1) Вариант 1
2) Вариант 2
3) Вариант 3
4) Вариант 4
Правильный ответ: X)

Используй только указанный формат. Не добавляй лишних символов или комментариев. Отправляй текстов в виде json файла как будто ты отправляешь мне json файл""",
                }
            ],
            "temperature": 1,
            "top_p": 0.1,
            "n": 1,
            "stream": False,
            "max_tokens": 2048,
            "repetition_penalty": 1,
            "update_interval": 0,
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {auth_token}",
    }
    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        # print("Ответ гигачата:\n", response)
        return response.json()
    except requests.RequestException as e:
        print(f"Произошла ошибка: {str(e)}")
        return None


def parse_quiz_text(quiz_text):
    questions = []
    print("Ответ гигачата:\n", quiz_text)
    # Заменяем символы \n на реальные символы новой строки
    quiz_text = quiz_text.replace("\\n", "\n")
    # Разделяем текст на блоки вопросов
    question_blocks = re.split(r"\n\s*\n", quiz_text.strip())
    
    for block in question_blocks:
        # Разделяем блок на строки
        lines = block.strip().split("\n")
        
        # Проверяем, что блок содержит достаточно строк для вопроса, вариантов и правильного ответа
        if len(lines) < 5:
            continue
        
        # Извлекаем вопрос (первая строка)
        question = lines[0].strip()
        
        # Извлекаем варианты ответов (строки, начинающиеся с "-")
        answers = []
        for line in lines[1:]:
            if line.strip().startswith("-"):
                answer = line.strip().split("- ")[1].strip()
                answers.append(answer)
            elif "Правильный ответ:" in line:
                break  # Прерываем цикл, если дошли до строки с правильным ответом
        
        # Извлекаем правильный ответ (последняя строка)
        correct_answer_line = lines[-1].strip()
        correct_answer_match = re.search(r"Правильный ответ: \*\*(.*?)\*\*", correct_answer_line)
        if not correct_answer_match:
            print(f"Ошибка: не удалось извлечь правильный ответ из строки: {correct_answer_line}")
            continue
        
        correct_answer_text = correct_answer_match.group(1).strip()
        
        # Формируем объект для вопроса
        questions.append({
            "question": question,
            "answers": answers,
            "correct_answer": correct_answer_text
        })
    
    return json.dumps(questions, indent=4, ensure_ascii=False)


def main(file_path):
    if not os.path.exists(file_path):
        print("Ошибка: файл не найден.")
        return

    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        text = process_pdf(file_path)
    elif ext == ".mp4":
        text = process_video(file_path)
    else:
        print("Ошибка: неподдерживаемый формат файла.")
        return

    giga_token = get_token()
    if not giga_token:
        print("Ошибка получения токена")
        return

    quiz_response = get_quiz_questions(giga_token, text)
    if not quiz_response:
        print("Ошибка генерации квиза")
        return
    
    # Извлекаем текст вопросов из ответа GigaChat
    quiz_text = quiz_response["choices"][0]["message"]["content"]
    
    # Сохраняем текст вопросов в файл
    # with open("giga_chat_response.txt", "w", encoding="utf-8") as f:
    #     f.write(quiz_text)

    # Парсим текст вопросов и преобразуем в JSON
    quiz_json = parse_quiz_text(quiz_text)
    print("Квиз JSON:")
    print(quiz_json)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python script.py <путь_к_файлу>")
    else:
        main(sys.argv[1])