import sys
import keyboard
import pyaudio
import wave
import datetime

# 음성 데이터 처리

MIC_DEVICE_ID = 1

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
SAMPLE_SIZE = 2 # FORMAT의 바이트 수

def record(record_seconds):
    p = pyaudio.PyAudio()
    stream = p.open(input_device_index = MIC_DEVICE_ID,
                    format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("Start to record the audio.")
    frames = []

    for i in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording is finished.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    return frames

# 녹음 데이터를 WAV 파일로 저장하기
def save_wav(target, frames):
    wf = wave.open(target, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(SAMPLE_SIZE)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

    if isinstance(target, str) : #  첫번째 문자가 문자열인지(파일인지 BytesIO인지 구분하기 위해)
        wf.close()

while True:
    if keyboard.is_pressed('ESC'): # ESC
        sys.exit()
    RECORD_SECONDS = 4
    frames = record(RECORD_SECONDS)

    now = datetime.datetime.now()
    WAVE_OUTPUT_FILENAME = f"{now.year}-{now.month}-{now.day}_{now.hour}-{now.minute}-{now.second}_output.wav"
    print(WAVE_OUTPUT_FILENAME)
    save_wav(WAVE_OUTPUT_FILENAME, frames)