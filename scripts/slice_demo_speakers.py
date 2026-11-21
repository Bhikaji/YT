import wave, numpy as np, os, imageio_ffmpeg
ff_dir = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
os.environ['PATH'] = ff_dir + os.pathsep + os.environ.get('PATH', '')

with wave.open('output/demo_audio_first40s.wav', 'rb') as w:
    sr = w.getframerate()
    audio = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)

from transformers import pipeline
pipe = pipeline('automatic-speech-recognition', model='openai/whisper-tiny')

for s in range(5, 35, 5):
    chunk = audio[int(s*sr):int((s+5)*sr)]
    res = pipe({'raw': chunk, 'sampling_rate': sr}, generate_kwargs={'language': 'mr', 'task': 'transcribe'})
    txt = res['text']
    print(f"{s:02d}s - {s+5:02d}s: {txt}")
