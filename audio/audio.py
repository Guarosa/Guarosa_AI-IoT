import cv2
import pyaudio
import wave
import datetime

# # 영상 데이터 처리
# cap = cv2.VideoCapture(0)		# 1번 카메라
#
# frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
#               int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# print('frame_size = ', frame_size)
#
# # fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
#
# out1 = cv2.VideoWriter('record0.mp4', fourcc, 20.0, frame_size)
# # out2 = cv2.VideoWriter('./data/record1.mp4', fourcc, 20.0, frame_size, isColor=False)
#
# while True:
#     retval, frame = cap.read()	# 프레임 캡처
#     if not retval: break
#
#     out1.write(frame)
#
#     # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     # out2.write(gray)
#     #
#     cv2.imshow('frame', frame)
#     # cv2.imshow('gray', gray)
#
#     key = cv2.waitKey(25)
#     if key == 27: break		# ESC
#
# cap.release()
# out1.release()
# # out2.release()
# #
# cv2.destroyAllWindows()

# 음성 데이터 처리

MIC_DEVICE_ID = 1

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
# RATE = 44100
RATE = 16000 # 카카오 음성인식에서 요구하는 RATE
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

# if __name__ == '__main__':
while True:
    # if key == 27: break  # ESC
    RECORD_SECONDS = 4
    frames = record(RECORD_SECONDS)

    now = datetime.datetime.now()
    WAVE_OUTPUT_FILENAME = f"../ {now.year}-{now.month}-{now.day};{now.hour}{now.minute}{now.second}-output.wav"
    print(WAVE_OUTPUT_FILENAME)
    save_wav(WAVE_OUTPUT_FILENAME, frames)