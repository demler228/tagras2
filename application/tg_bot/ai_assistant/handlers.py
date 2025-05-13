import os
import re
import logging
from glob import glob
from difflib import SequenceMatcher
from pathlib import Path
from docx import Document as DocxDocument
from pypdf import PdfReader
from moviepy.editor import VideoFileClip
import whisper
from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from gigachat import GigaChat
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from application.tg_bot.ai_assistant.keyboards.get_exit_button import get_exit_button_ai
from application.tg_bot.filters.is_admin import is_admin
from application.tg_bot.menu.personal_actions.keyboards.menu_keyboard import get_main_menu_keyboard
from aiogram.types.input_file import FSInputFile

logging.basicConfig(
    filename='assistant.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

auth = "Y2U3MmFkYTEtMGIzNC00M2UwLTliNGYtYjRhMGFhODUzYTFhOjlmYzZlMmE2LTIyMDMtNDE4NC1iNWExLTA4ZjUyNTk1YjE3OQ=="
giga = GigaChat(
    credentials=auth,
    model='GigaChat:latest',
    verify_ssl_certs=False
)

whisper_model = whisper.load_model("base")

class AIState(StatesGroup):
    active = State()

router = Router()

vectorstore = None

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def remove_empty_lines(text):
    return "\n".join(line for line in text.splitlines() if line.strip())

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

def process_pdf(pdf_path):
    try:
        text = ""
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return clean_text(text)
    except Exception as e:
        logging.error(f"Ошибка обработки PDF {pdf_path}: {e}")
        return ""

def process_docx(docx_path):
    try:
        doc = DocxDocument(docx_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return remove_empty_lines(text)
    except Exception as e:
        logging.error(f"Ошибка обработки DOCX {docx_path}: {e}")
        return ""

def process_video(video_path):
    try:
        temp_audio = "temp_audio.wav"
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(temp_audio)
        
        result = whisper_model.transcribe(temp_audio)
        
        os.remove(temp_audio)
        video.close()
        
        return clean_text(result["text"])
    except Exception as e:
        logging.error(f"Ошибка обработки видео {video_path}: {e}")
        return ""

def load_documents():
    docs = []
    
    materials_path = Path("D:/zilant_projects/quiz/employee_adaptation_project/application/tg_bot/ai_assistant/materials")
    if not materials_path.exists():
        logging.error(f"Папка {materials_path} не найдена!")
        return docs
    
    for pdf_path in materials_path.glob("*.pdf"):
        try:
            logging.info(f"Обработка PDF: {pdf_path}")
            text = process_pdf(pdf_path)
            if text:
                docs.append(Document(
                    page_content=text,
                    metadata={"source": str(pdf_path), "type": "pdf"}
                ))
        except Exception as e:
            logging.error(f"Ошибка при обработке PDF {pdf_path}: {e}")
    
    for docx_path in materials_path.glob("*.docx"):
        try:
            logging.info(f"Обработка DOCX: {docx_path}")
            text = process_docx(docx_path)
            if text:
                docs.append(Document(
                    page_content=text,
                    metadata={"source": str(docx_path), "type": "docx"}
                ))
        except Exception as e:
            logging.error(f"Ошибка при обработке DOCX {docx_path}: {e}")
    
    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv']
    for ext in video_extensions:
        for video_path in materials_path.glob(ext):
            try:
                logging.info(f"Обработка видео: {video_path}")
                text = process_video(video_path)
                if text:
                    docs.append(Document(
                        page_content=f"[ВИДЕО {video_path.name}]:\n{text}",
                        metadata={"source": str(video_path), "type": "video"}
                    ))
            except Exception as e:
                logging.error(f"Ошибка при обработке видео {video_path}: {e}")
    
    logging.info(f"Загружено {len(docs)} файлов (документы и видео)")
    return docs

def create_vector_store(docs):
    if not docs:
        logging.warning("Нет документов для обработки")
        return None
    
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len,
        )
        
        splits = text_splitter.split_documents(docs)
        
        embeddings = HuggingFaceEmbeddings(
            model_name="cointegrated/LaBSE-en-ru"
        )
        
        return FAISS.from_documents(splits, embeddings)
    except Exception as e:
        logging.error(f"Ошибка при создании векторного хранилища: {e}")
        return None

def initialize_vector_store():
    global vectorstore
    docs = load_documents()
    vectorstore = create_vector_store(docs)
    if vectorstore:
        logging.info("Векторное хранилище успешно инициализировано")
    else:
        logging.error("Не удалось создать векторное хранилище")

@router.callback_query(F.data == "ai_assistant_button")
async def handle_ai_assistant_button(callback_query: types.CallbackQuery, state: FSMContext):
    global vectorstore
    
    if vectorstore is None:
        msg = await callback_query.message.answer("Идёт инициализация базы знаний...")
        initialize_vector_store()
        await msg.delete()
        if vectorstore is None:
            await callback_query.message.answer(
                "Не удалось загрузить базу знаний. Попробуйте позже.",
                reply_markup=get_exit_button_ai()
            )
            return
    
    await state.set_state(AIState.active)
    await callback_query.message.answer(
        "Привет! Я ваш виртуальный помощник в компании Таграс.\n"
        "Можете задать мне вопрос о документах, видеофайлах или просто пообщаться.",
        reply_markup=get_exit_button_ai()
    )

@router.message(F.text, AIState.active)
async def handle_text_message(message: Message, state: FSMContext):
    user_input = message.text

    if user_input.lower() in ["вернуться в меню", "выход"]:
        await message.answer("Режим общения с ИИ деактивирован.\n\nДобро пожаловать в меню", 
                            reply_markup=get_main_menu_keyboard(is_admin(message.from_user.id)))
        await state.clear()
        return

    try:
        if not vectorstore:
            await message.answer(
                "База знаний не загружена. Попробуйте позже.",
                reply_markup=get_exit_button_ai()
            )
            return

        # Получаем наиболее релевантные документы
        relevant_docs = vectorstore.similarity_search(user_input, k=4)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # Получаем пути к исходным файлам из метаданных
        source_files = list(set([doc.metadata["source"] for doc in relevant_docs if "source" in doc.metadata]))
        
        system_prompt = (
            "Ты - ассистент компании Таграс. Отвечай на вопросы на основании предоставленных документов. "
            "Если информация не найдена в документах, то постарайся ответить сам, но ничего лишнего кроме, "
            "работы связанной с Таграс не говори. В контексте могут встречаться расшифровки видео - учитывай их тоже."
        )
        
        user_prompt = f"""
        Контекст:
        {context}
        
        Вопрос:
        {user_input}
        
        Ответь максимально точно на основе предоставленного контекста.
        Если в контексте есть ссылки на видео, укажи это в ответе.
        """
        
        response = giga.chat(system_prompt + "\n" + user_prompt)
        answer = response.choices[0].message.content
        
        # Отправляем текстовый ответ
        await message.answer(answer, reply_markup=get_exit_button_ai())
        
        # Отправляем исходные файлы, если они есть
        if source_files:
            await message.answer("Вот документы, которые могут содержать полезную информацию:")
            
            for file_path in source_files:
                try:
                    # Проверяем существование файла
                    if not os.path.exists(file_path):
                        continue
                        
                    # Определяем тип файла
                    file_ext = file_path.split('.')[-1].lower()
                    file_name = os.path.basename(file_path)
                    
                    # Отправляем файл пользователю
                    if file_ext in ['pdf', 'docx']:
                        file = FSInputFile(file_path, filename=file_name)
                        if file_ext == 'pdf':
                            await message.answer_document(file, caption=f"PDF файл: {file_name}")
                        else:
                            await message.answer_document(file, caption=f"Word документ: {file_name}")
                    elif file_ext in ['mp4', 'avi', 'mov', 'mkv']:
                        file = FSInputFile(file_path, filename=file_name)
                        await message.answer_video(file, caption=f"Видео файл: {file_name}")
                    
                except Exception as e:
                    logging.error(f"Ошибка при отправке файла {file_path}: {e}")
                    await message.answer(f"Не удалось отправить файл {file_name}")
        
    except Exception as e:
        logging.error(f"Ошибка при обработке запроса: {e}")
        await message.answer(
            "Произошла ошибка при обработке запроса. Попробуйте переформулировать вопрос.",
            reply_markup=get_exit_button_ai()
        )
initialize_vector_store()