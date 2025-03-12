import whisper
import moviepy as mp

clip = mp.VideoFileClip(r'test_video.mp4')
clip.audio.write_audiofile(r'audio_test.mp3')

model = whisper.load_model("base")
result = model.transcribe("D:/zilant_projects/tagras/audio_test.mp3",fp16=False)
print(result["text"])