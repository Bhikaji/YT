import os, glob, wave, numpy as np, imageio_ffmpeg, subprocess
ff_dir = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
os.environ['PATH'] = ff_dir + os.pathsep + os.environ.get('PATH', '')

from transformers import pipeline
pipe = pipeline('automatic-speech-recognition', model='openai/whisper-tiny')

exe = imageio_ffmpeg.get_ffmpeg_exe()
for mp3 in sorted(glob.glob('output/voice_benchmark/*.mp3')):
    wav = mp3.replace('.mp3', '.wav')
    subprocess.run([exe, "-y", "-i", mp3, "-ar", "16000", "-ac", "1", wav], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    with wave.open(wav, 'rb') as w:
        raw = w.readframes(w.getnframes())
        arr = np.frombuffer(raw, dtype=np.int16).astype(np.float32)/32768.0
    res = pipe({'raw': arr, 'sampling_rate': 16000}, generate_kwargs={'language': 'mr', 'task': 'transcribe'})
    print(f"{os.path.basename(mp3)}:")
    print("  ASR:", res["text"])
