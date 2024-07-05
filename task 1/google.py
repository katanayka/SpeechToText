import speech_recognition as sr

def google(audio):
    recognizer = sr.Recognizer()
    response = {
        "success": True,
        "error": None,
        "transcription": ""
    }
    try:
        response["transcription"] = recognizer.recognize_google(audio, language='ru-RU')
    except sr.RequestError:
        response["success"] = False
        response["error"] = f"API google недоступно"
    except sr.UnknownValueError:
        response["success"] = False
        response["error"] = "Не удалось распознать речь"
    return response
