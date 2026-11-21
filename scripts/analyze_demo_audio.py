import os
import wave
import numpy as np
import imageio_ffmpeg

ff_dir = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
os.environ["PATH"] = ff_dir + os.pathsep + os.environ.get("PATH", "")

from transformers import pipeline

with wave.open("output/demo_audio_first40s.wav", "rb") as w:
    sr = w.getframerate()
    n_frames = w.getnframes()
    raw = w.readframes(n_frames)
    audio_arr = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

pipe = pipeline("automatic-speech-recognition", model="openai/whisper-tiny")

seg_samples = int(25 * sr)
audio_seg = audio_arr[:seg_samples]

res = pipe({"raw": audio_seg, "sampling_rate": sr}, generate_kwargs={"language": "mr", "task": "transcribe"})
print("Transcription (0-25s in Marathi):")
print(res["text"])

seg2 = audio_arr[int(15*sr):int(35*sr)]
res2 = pipe({"raw": seg2, "sampling_rate": sr}, generate_kwargs={"language": "mr", "task": "transcribe"})
print("Transcription (15-35s in Marathi):")
print(res2["text"])
