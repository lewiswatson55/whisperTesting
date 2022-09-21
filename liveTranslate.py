import sounddevice as sd
import soundfile as sf
import uuid
import time, os
import whisper

model = whisper.load_model("large")
print("Model loaded")

def delete_audio(uuid):
    os.remove(f"raw_audio/{uuid}.wav")

def transcribe_audio(uuid):
    print("Transcribing audio")
    audio = whisper.load_audio(f"raw_audio/{uuid}.wav")
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")
    options = whisper.DecodingOptions(task="translate")
    result = whisper.decode(model, mel, options)
    delete_audio(uuid)

    print(result.text)

samplerate = 44100  # Hertz
duration = 5  # seconds



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