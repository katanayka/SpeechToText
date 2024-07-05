import speech_recognition as sr
import os
from sber import recognize_speech_sber
from openai import openai
from google import google
import string
import time

def record_audio(recognizer, microphone, save_path=None):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Скажите что-нибудь...")
        audio = recognizer.listen(source)
    if save_path:
        with open(save_path, "wb") as f:
            f.write(audio.get_wav_data())
    return audio

def load_audio(file_path): # подгоянет аудио под формат с которым рекогнайзер может работать
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    return audio

def generate_response(text):
    text = text.translate(str.maketrans('', '', string.punctuation)) # стираем пунктуацию
    if text.lower() == "привет я разработчик":
        return "сегодня выходной"
    elif text.lower() == "я сегодня не приду домой":
        return "Ну и катись отсюда"
    else:
        return "Фраза не распознана"

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    choice = input("Введите '1' для записи аудио, '2' для загрузки аудио файла: ")
    
    if choice == '1':
        audio = record_audio(recognizer, microphone, save_path="./task 1/recorded_audio.wav")
    elif choice == '2':
        file_path = input("Введите путь к аудио файлу: ")
        if not os.path.exists(file_path):
            print("Файл не найден!")
            return
        audio = load_audio(file_path)
    else:
        print("Неверный выбор!")
        return

    apis = ['google', 'sber', 'openai']
    for api in apis:
        start_time = time.time()
        if api == 'google':
            response = google(audio)
        elif api == 'sber':
            response = recognize_speech_sber(audio)
        elif api == 'openai':
            response = openai("./task 1/recorded_audio.wav") if choice == "1" else openai("./task 1/test.wav")
        print(f"Результат с API '{api}':")
        if response["success"]:
            print("Вы сказали: {}".format(response["transcription"]))
            reply = generate_response(response["transcription"])
            print("Ответ: {}".format(reply))
        else:
            print("Ошибка: {}".format(response["error"]))
        end_time = time.time()
        print('Прошло: ', end_time - start_time)   

if __name__ == "__main__":
    main()
