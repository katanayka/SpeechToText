from pyannote.audio import Pipeline
from scipy.io import wavfile
import speech_recognition as sr
from sber import recognize_speech_sber

def load_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    return audio

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="use_auth_token") 

import torch
pipeline.to(torch.device("cuda"))

diarization = pipeline("./task 2/audio.wav")
rate, data = wavfile.read('./task 2/audio.wav') 
wavfile.write(f'./task 2/right_temp.wav', rate, data) # сделал копию чтоб не вредить оригинальной записи 

stop_last = 0
for turn, _, speaker in diarization.itertracks(yield_label=True): # содержит инфу по промежуткам времени где была чья-то речь
    rate, data = wavfile.read('./task 2/right_temp.wav') 
    split_at_frame = rate * (turn.end-stop_last) 
    split_at_frame = int(split_at_frame)
    left_data, right_data = data[:split_at_frame-1], data[split_at_frame:] # разделяем на до и после окончания речи

    wavfile.write(f'./task 2/left_temp.wav', rate, left_data)
    wavfile.write(f'./task 2/right_temp.wav', rate, right_data)

    audio = load_audio("./task 2/left_temp.wav")
    recognizer = sr.Recognizer()
    try:
      print(recognize_speech_sber(audio), speaker) # левую часть переводим, далее по кусочкам разбираем правую
    except:
      pass
    stop_last = turn.end

def load_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    return audio
