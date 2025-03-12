import os
import re
import sys
import whisper
from pdfminer.high_level import extract_text
import moviepy as mp

def remove_empty_lines(text):
    lines = [line for line in text.splitlines() if line.strip()]
    return '\n'.join(lines)

def process_pdf(pdf_path):
    text = extract_text(pdf_path)
    return remove_empty_lines(text)

def process_video(video_path, audio_path="audio_temp.mp3"):
    clip = mp.VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, codec='mp3')
    
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, fp16=False)
    
    os.remove(audio_path)
    return result["text"]

def main(file_path):
    if not os.path.exists(file_path):
        print("Ошибка: файл не найден.")
        return
    
    ext = os.path.splitext(file_path)[-1].lower()
    
    if ext == ".pdf":
        text = process_pdf(file_path)
        print("Распознанный текст из PDF:\n", text)
    elif ext == ".mp4":
        text = process_video(file_path)
        print("Распознанная речь из видео:\n", text)
    else:
        print("Ошибка: неподдерживаемый формат файла.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python script.py <путь_к_файлу>")
    else:
        main(sys.argv[1])
