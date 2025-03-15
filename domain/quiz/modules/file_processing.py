import os
from pdfminer.high_level import extract_text
from docx import Document
import moviepy as mp
from modules.utils import remove_empty_lines
import whisper


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


def process_file(file_path):
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        return process_pdf(file_path)
    elif ext == ".mp4":
        return process_video(file_path)
    elif ext == ".docx":
        return process_docx(file_path)
    else:
        return None