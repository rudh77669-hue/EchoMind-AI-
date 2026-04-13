import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import io
import soundfile as sf

def audio(file_storage):
    # Read raw bytes from Flask FileStorage
    audio_bytes = file_storage.read()
    audio, sampling_rate = sf.read(io.BytesIO(audio_bytes))

    # Resample to 16k if needed
    if sampling_rate != 16000:
        audio = librosa.resample(audio, orig_sr=sampling_rate, target_sr=16000)
        sampling_rate = 16000

    # Process with Wav2Vec2
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

    input_values = processor(audio, sampling_rate=16000, return_tensors="pt").input_values
    with torch.no_grad():
        logits = model(input_values).logits

    predicted_ids = torch.argmax(logits, dim=-1)
    transcript = processor.decode(predicted_ids[0])

    print("📝 Transcript:", transcript)
    return transcript
