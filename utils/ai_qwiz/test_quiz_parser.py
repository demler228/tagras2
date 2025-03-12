import os
import json
import sys
import whisper
import requests
import uuid
from pdfminer.high_level import extract_text
import moviepy as mp
from docx import Document   
import requests
from bs4 import BeautifulSoup

client_id = "ce7d7680-4bf7-4ff3-b172-3be3794aa5b8"
secret = "338c3cfd-1038-4d2b-9e27-5af3a3d7f728"
auth = "Y2U3ZDc2ODAtNGJmNy00ZmYzLWIxNzItM2JlMzc5NGFhNWI4OjMzOGMzY2ZkLTEwMzgtNGQyYi05ZTI3LTVhZjNhM2Q3ZjcyOA=="


def remove_empty_lines(text):
    return "\n".join(line for line in text.splitlines() if line.strip())


def process_pdf(pdf_path):
    text = extract_text(pdf_path)
    return remove_empty_lines(text)

def process_docx(docx_path):
    doc = Document(docx_path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return remove_empty_lines(text)

def process_video(video_path, audio_path="audio_temp.mp3"):
    clip = mp.VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, codec="mp3")

    model = whisper.load_model("base")
    result = model.transcribe(audio_path, fp16=False)

    os.remove(audio_path)
    return result["text"]

def process_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator="\n")
        return remove_empty_lines(text)
    except requests.RequestException as e:
        print(f"Ошибка при загрузке страницы: {e}")
        return None


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
- Вопрос
- 4 варианта ответа (пронумерованные от 1 до 4)
- Правильный ответ (указанный в формате "Правильный ответ: X)")

Верни ответ в формате JSON, как в примере ниже:

[
    {{
        "question": "Почему Бу не смог провести успешные переговоры с американцами?",
        "answers": [
            "Он не знал английский язык.",
            "Он не подготовился к переговорам.",
            "Он не смог договориться с американцами.",
            "Он не был уверен в себе."
        ],
        "correct_answer": "Он не подготовился к переговорам."
    }},

Убедись, что ответ строго соответствует этому формату JSON. Не добавляй лишних символов или комментариев.""",
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
        return response.json()
    except requests.RequestException as e:
        print(f"Произошла ошибка: {str(e)}")
        return None

def main(file_path):
    if not os.path.exists(file_path):
        print("Ошибка: файл не найден.")
        return

    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        text = process_pdf(file_path)
    elif ext == ".mp4":
        text = process_video(file_path)
    elif ext == ".docx":
        text = process_docx(file_path)
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
    
    quiz_text = quiz_response["choices"][0]["message"]["content"]
    
    try:
        quiz_json = json.loads(quiz_text)
        print("Квиз JSON:")
        print(json.dumps(quiz_json, indent=4, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print(f"Ошибка: не удалось преобразовать ответ в JSON: {e}")
        print("Ответ GigaChat:")
        print(quiz_text)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python script.py <путь_к_файлу>")
    else:
        main(sys.argv[1])