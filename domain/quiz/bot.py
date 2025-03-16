import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from main import main as generate_quiz  # Импортируем вашу основную функцию
import json

# Настройка логирования
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен вашего бота
TELEGRAM_TOKEN = "7607849811:AAFYhxA4077tQqHbCdc6zDxU2iFPP34xU1k"

# Глобальные переменные для хранения материалов и квизов
user_materials = {}
user_quizzes = {}

# Команда /start
async def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_materials[user_id] = []  # Инициализация списка материалов для пользователя
    user_quizzes[user_id] = None  # Инициализация квиза для пользователя

    keyboard = [["Обучение", "Квиз"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите раздел:", reply_markup=reply_markup)

# Обработка кнопки "Обучение"
async def handle_learning(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Отправьте материалы для обучения (видео, PDF, Word, ссылки). "
        "Когда закончите, нажмите /done."
    )

# Скачивание файла
async def download_file(file_id, file_name, context: CallbackContext):
    file = await context.bot.get_file(file_id)
    file_path = os.path.join("downloads", file_name)
    await file.download_to_drive(file_path)
    return file_path

# Обработка загруженных материалов
async def handle_materials(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    # Инициализация user_materials[user_id], если он не существует
    if user_id not in user_materials:
        user_materials[user_id] = []

    file = update.message.document or update.message.video or update.message.text

    if file:
        if update.message.document:
            file_id = update.message.document.file_id
            file_name = update.message.document.file_name
            file_path = await download_file(file_id, file_name, context)
        elif update.message.video:
            file_id = update.message.video.file_id
            file_name = "video.mp4"
            file_path = await download_file(file_id, file_name, context)
        else:
            file_id = None
            file_name = update.message.text
            file_path = file_name  # Для ссылок используем текст как путь

        # Сохраняем материал
        user_materials[user_id].append((file_path, file_name))
        await update.message.reply_text(f"Материал '{file_name}' добавлен.")
    else:
        await update.message.reply_text("Неподдерживаемый формат файла.")

# Команда /done для завершения загрузки материалов
async def done(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    # Инициализация user_materials[user_id], если он не существует
    if user_id not in user_materials:
        user_materials[user_id] = []

    await update.message.reply_text(
        f"Загрузка материалов завершена. Всего материалов: {len(user_materials[user_id])}."
    )

# Отправка вопросов и ответов
async def send_quiz_questions(update: Update, quiz_result):
    for question_data in quiz_result:
        question = question_data["question"]
        answers = "\n".join([f"{i + 1}. {answer}" for i, answer in enumerate(question_data["answers"])])
        message = f"❓ Вопрос:\n{question}\n\n📝 Варианты ответов:\n{answers}"
        await update.message.reply_text(message)

# Обработка кнопки "Квиз"
async def handle_quiz(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    # Инициализация user_materials[user_id], если он не существует
    if user_id not in user_materials:
        user_materials[user_id] = []

    if not user_materials[user_id]:
        await update.message.reply_text("Сначала загрузите материалы в разделе 'Обучение'.")
        return

    # Генерация квиза
    materials = [material[0] for material in user_materials[user_id]]  # Используем пути к файлам/ссылкам
    quiz_result = generate_quiz(materials)

    if quiz_result:
        user_quizzes[user_id] = quiz_result
        await update.message.reply_text("Квиз сгенерирован! Вот вопросы:")
        await send_quiz_questions(update, quiz_result)  # Отправляем вопросы и ответы
    else:
        await update.message.reply_text("Ошибка генерации квиза.")

# Запуск бота
def main():
    # Создаем папку для загрузок, если её нет
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex("^Обучение$"), handle_learning))
    application.add_handler(MessageHandler(filters.Regex("^Квиз$"), handle_quiz))
    application.add_handler(MessageHandler(filters.Document.ALL | filters.VIDEO | filters.TEXT, handle_materials))
    application.add_handler(CommandHandler("done", done))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()