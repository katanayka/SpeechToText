import requests
import speech_recognition as sr
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_token_sber(uid, secret):
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        "Authorization": f"Basic {secret}",
        "RqUID": f"{uid}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "scope": "SALUTE_SPEECH_PERS"
    }
    response = requests.post(url, headers=headers, data=data, verify=False)
    token = response.json()["access_token"]
    return token

def recognize_speech_sber(audio):
    audio_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
    uid = "uid"
    secret = "secret"
    token = get_token_sber(uid, secret)
    url = "https://smartspeech.sber.ru/rest/v1/speech:recognize"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "audio/x-pcm;bit=16;rate=16000"
    }
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    try:
        res = requests.post(url, headers=headers, data=audio_data, verify=False)
        res.raise_for_status()
        response["transcription"] = res.json()["result"][0]
    except requests.RequestException as e:
        response["success"] = False
        response["error"] = str(e)
    return response