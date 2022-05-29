import pyttsx3 as p
import speech_recognition as sr
import apiai, json, re
from refactor.extractor import NumberExtractor
#import neuro_comma_master.src.main
from neuro_comma_master.src.neuro_comma.cache import ModelCache
import soundfile
import wave
import io
from pydub import AudioSegment
from scipy.io.wavfile import write
import numpy as np

engine = p.init()
rate = engine.getProperty('rate') #Скорость произношения
engine.setProperty('rate', rate-70)
volume = engine.getProperty('volume') #Громкость голоса
engine.setProperty('volume', volume+0.9)
voices = engine.getProperty('voices')
# Задать голос по умолчанию
engine.setProperty('voice', 'ru')
# Попробовать установить предпочтительный голос
for voice in voices:
    if voice.name == 'Tatiana':
        engine.setProperty('voice', voice.id)

# Создаем объект для рефакторинга чисел
#extractor = NumberExtractor()

# Функция восстановления пункутации
def get_punctuation_restoration(data):
    model = ModelCache().model
    if isinstance(data, str):
        output_data = model(data)
    else:
        output_data = [model(text) for text in data]  # type: ignore
    return output_data

def speak(text):
    engine.say(text)
    engine.runAndWait()

#speak("Привет, меня зовут Таня и я помощник твоего здоровья.")

nchannels = 1
sampwidth = 1
framerate = 8000
nframes = 1

def to_text(ogg: bytes):
    extractor = NumberExtractor()
    #data, samplerate = soundfile.read(ogg)
    #soundfile.write('in.wav', data, samplerate)
    #data, samplerate = soundfile.read("voices//in.wav")
    name = 'output.wav'
    audioW = wave.open(name, 'wb')
    audioW.setnchannels(nchannels)
    audioW.setsampwidth(sampwidth)
    audioW.setframerate(framerate)
    audioW.setnframes(nframes)
    blob = ogg
    #data, samplerate = soundfile.read(io.BytesIO(ogg),format='RAW', channels=2, sample rate=8000,
     #                      subtype='PCM_16')
    audioW.writeframes(blob)
    #data = b''.join(ogg)
    #ad = sr.AudioFile(name)
    '''s = io.BytesIO(ogg)
    audio = AudioSegment.from_raw(s, sample_width=1, frame_rate=16000, channels=1).export(name, format='wav')'''
    '''bytes_wav = bytes()
    byte_io = io.BytesIO(bytes_wav)
    write(byte_io, 16000, np.frombuffer(ogg, dtype=np.int16))
    output_wav = byte_io.read()
    output, samplerate = soundfile.read(io.BytesIO(output_wav))
    write("output1.wav", 16000, output)'''
    ad = sr.AudioFile(name)
    #ad = sr.AudioData(ogg, 16000, 2)
    r = sr.Recognizer()

    try:
        s = r.recognize_google(ad, language = 'ru-RU')
        text = s.lower()
        text = text[:1].upper() + text[1:]
        text, mask = extractor.replace(text, apply_regrouping=True)  # Заменяем на цифры
        #text = get_punctuation_restoration(text)
        print("Text: " + text)
        return text
    except Exception as e:
        print("Exception: " + str(e))

def talk_to_file(str):
    engine.save_to_file(str, "voices//speech.wav")
    data, samplerate = soundfile.read("voices//speech.wav")
    return data


def record_volume():
    r = sr.Recognizer()
    extractor = NumberExtractor()
    with sr.Microphone(device_index = 1) as source:
        print('Настраиваюсь.')
        r.adjust_for_ambient_noise(source, duration=1)
        print('Слушаю...')
        audio = r.listen(source)
    print('Услышала.')
    try:
        query = r.recognize_google(audio, language = 'ru-RU')
        text = query.lower()
        text = text[:1].upper() + text[1:]
        text, mask = extractor.replace(text, apply_regrouping=True) # Заменяем на цифры
        #text = get_punctuation_restoration(text)
        print(f'Вы сказали: {text}')
        textMessage( text )
    except:
        print('Ошибка распознавания.')


def talk( text ):
    engine.say( text )
    engine.runAndWait()

def textMessage( text ):
    request = apiai.ApiAI('7236207208265215800217565610').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'ваш id' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем пользователю, если нет - бот его не понял
    if response:
        request.audio_output = response
        talk(response)
    else:
        talk('Простите. Я Вас не совсем поняла.')




#while True:
#    record_volume()



