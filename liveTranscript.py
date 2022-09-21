import sounddevice as sd
import soundfile as sf
import uuid
import time
import whisper
import os

model = whisper.load_model("large")
print("Model loaded")

decodeoptions = whisper.DecodingOptions(task="translate")

def transcribe_audio(uuid):
    print("Transcribing audio")
    result = model.transcribe(f"raw_audio/{uuid}.wav", decodeoptions)
    print(result["text"])

samplerate = 44100  # Hertz
duration = 5  # seconds

def delete_audio(uuid):
    os.remove(f"raw_audio/{uuid}.wav")

while True:
    print("Recording...")
    _uuid = uuid.uuid4()
    filename = "raw_audio/" + str(_uuid) + '.wav'
    mydata = sd.rec(int(samplerate * duration), samplerate=samplerate,
                    channels=2, blocking=True)
    print("Done recording")
    sf.write(filename, mydata, samplerate)
    print("Saved to " + filename)
    transcribe_audio(_uuid)
    #time.sleep(duration)