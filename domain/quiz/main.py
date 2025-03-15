import os
import sys
from modules.file_processing import process_file
from modules.web_processing import process_url
from modules.gigachat_api import get_quiz_questions, get_token
from modules.utils import add_incorrect_answers
from modules.send_data_todb import send_to_db
import json


def process_material(material):
    if material.startswith("http://") or material.startswith("https://"):
        text = process_url(material)
        if not text:
            print(f"Ошибка: не удалось загрузить текст по ссылке: {material}")
            return None
    else:
        if not os.path.exists(material):
            print(f"Ошибка: файл не найден: {material}")
            return None
        text = process_file(material)
        if not text:
            print(f"Ошибка: неподдерживаемый формат файла: {material}")
            return None
    return text


def main(materials):
    all_texts = []
    theme = input("Введите тему для квиза (например, 'Информационная безопасность'): ").strip()
    if not theme:
        print("Ошибка: тема не может быть пустой.")
        return

    for material in materials:
        text = process_material(material)
        if text:
            all_texts.append(text)
    
    if not all_texts:
        print("Ошибка: ни один материал не был успешно обработан.")
        return

    combined_text = "\n".join(all_texts)

    giga_token = get_token()
    if not giga_token:
        print("Ошибка получения токена")
        return

    while True:
        quiz_response = get_quiz_questions(giga_token, combined_text)
        if not quiz_response:
            print("Ошибка генерации квиза")
            return
        
        quiz_text = quiz_response["choices"][0]["message"]["content"]
        
        try:
            quiz_json = json.loads(quiz_text)
            quiz_json = add_incorrect_answers(quiz_json)
            print("Квиз JSON:")
            print(json.dumps(quiz_json, indent=4, ensure_ascii=False))
            send_to_db(quiz_json, theme)
            return quiz_json
        except json.JSONDecodeError as e:
            print(f"Ошибка: не удалось преобразовать ответ в JSON: {e}")
            print("Ответ GigaChat:")
            print(quiz_text)
            retry = input("Хотите попробовать сгенерировать квиз еще раз? (да/нет): ").lower()
            if retry != 'да':
                print("Генерация квиза прекращена.")
                break


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python main.py <путь_к_файлу_или_ссылка1> <путь_к_файлу_или_ссылка2> ...")
    else:
        main(sys.argv[1:])