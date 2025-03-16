import os
import sys
import json
from db_bl import FileService, WebService, QuizService, DBService
from db_dal import QuizRepository
from modules.utils import add_incorrect_answers

def process_material(material: str):
    if material.startswith("http://") or material.startswith("https://"):
        text = WebService.process_url(material)
        if not text:
            print(f"Ошибка: не удалось загрузить текст по ссылке: {material}")
            return None
    else:
        if not os.path.exists(material):
            print(f"Ошибка: файл не найден: {material}")
            return None
        text = FileService.process_file(material)
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

    giga_token = QuizRepository.get_token()
    if not giga_token:
        print("Ошибка получения токена")
        return

    while True:
        quiz_response = QuizService.generate_quiz(giga_token, combined_text)
        if not quiz_response:
            print("Ошибка генерации квиза")
            retry = input("Хотите попробовать сгенерировать квиз еще раз? (да/нет): ").lower()
            if retry != 'да':
                print("Генерация квиза прекращена.")
                break
        else:
            print("Квиз JSON:")
            print(json.dumps(quiz_response, indent=4, ensure_ascii=False))

            quiz_json_str = quiz_response["choices"][0]["message"]["content"]
            try:
                quiz_data = json.loads(quiz_json_str)
                quiz_data = add_incorrect_answers(quiz_data)
                print("Распарсенный квиз:")
                print(json.dumps(quiz_data, indent=4, ensure_ascii=False))

                DBService.save_quiz(quiz_data, theme)
                return quiz_data
            except json.JSONDecodeError as e:
                print(f"Ошибка: не удалось распарсить JSON: {e}")
                print("Ответ GigaChat:")
                print(quiz_json_str)
                retry = input("Хотите попробовать сгенерировать квиз еще раз? (да/нет): ").lower()
                if retry != 'да':
                    print("Генерация квиза прекращена.")
                    break


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python main.py <путь_к_файлу_или_ссылка1> <путь_к_файлу_или_ссылка2> ...")
    else:
        main(sys.argv[1:])