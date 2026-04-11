#imports
import numpy as np
import whisper
import pyaudio
from openwakeword.model import Model
import sounddevice as sd
import soundfile as sf
import time
import torch
import edge_tts
import asyncio
from Langchain_agent import ask_ai

#model init
vad_model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad')
(get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils
speech_model = whisper.load_model("base.en")
model = Model(wakeword_models=[r"./model/jarvis_v2.onnx"],inference_framework="onnx") 


#audio init
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000          
CHUNK = 512
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
running = False

#Wake_word
def wake_word():
    
    print('listening')
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_frame = np.frombuffer(data, dtype=np.int16)
        prediction = model.predict(audio_frame)

        for wakeword, score in prediction.items():
            if score > 0.35:
                return True

#speech recognition
def speech_recognition():

    vad_iterator = VADIterator(vad_model)
    frames = []

    max_duration = 15 
    start_time = time.time()
    
    while (time.time() - start_time) < max_duration:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio = np.frombuffer(data, dtype=np.int16)
        frames.append(audio)
        audio_32 = audio.astype(np.float32) / 32768.0
        
        speech_dict = vad_iterator(torch.from_numpy(audio_32), return_seconds=True)
        if speech_dict:
            if 'end' in speech_dict:
                print("Silence detected, stopping recording.")
                break


    audio_data = np.concatenate(frames).astype(np.float32) / 32768.0

    result = speech_model.transcribe(audio_data, fp16=False)
    return result['text']

#Play Audio's By File
def play_audio(filename):
    data, fs = sf.read(filename, dtype='float32')
    sd.play(data, fs)
    sd.wait() 

#Async Function To Generate and Speak TTS
async def tts(speech):
    communicate = edge_tts.Communicate(speech, "en-US-GuyNeural")
    await communicate.save("output.mp3")

#The Full Script To Run Jarvis
def run_jarvis():

    while True:
        if wake_word():

            #inform User that they have heard Jarvis
            print('Heard Jarvis')

            #recognize the user's speech
            speech = speech_recognition()
            print(f'Heard: {speech}')

            #Ai response
            response = ask_ai(speech)
            print('Ai: ', response)

            #Playing the tts
            asyncio.run(tts(response))
            play_audio(r'output.mp3')
            
            model.reset()

run_jarvis()
