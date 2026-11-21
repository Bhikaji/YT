import sys
sys.path.insert(0, 'third_party/whisperx')
import whisperx

print("Loading WhisperX...")
model = whisperx.load_model('small', 'cpu', compute_type='int8')
audio = whisperx.load_audio('crockdile_inspect/crockdile_audio.wav')
result = model.transcribe(audio, batch_size=4)
print("Language detected:", result.get("language"))
for seg in result["segments"]:
    print(f"[{seg['start']:.2f}s - {seg['end']:.2f}s]: {seg['text']}")
