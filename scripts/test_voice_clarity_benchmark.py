import asyncio
import edge_tts
import imageio_ffmpeg, os, subprocess

ff_dir = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
os.environ["PATH"] = ff_dir + os.pathsep + os.environ.get("PATH", "")

lines = [
    ("mother", "mr-IN-AarohiNeural", "+0%", "+0Hz", "बब्या, शांत बैस तिथं! काय गडबड केली ना, तर घरी आल्यावर बघ!"),
    ("mother_scold", "mr-IN-AarohiNeural", "-2%", "+4Hz", "तवा मस्त्या कराल का? माझ्या बापाचं गाव काय?"),
    ("bob_manohar_fast", "mr-IN-ManoharNeural", "+4%", "+15Hz", "अगं माय, काय नाय केलं मी! शांतच तर बसलोय!"),
    ("bob_manohar_natural", "mr-IN-ManoharNeural", "+0%", "+0Hz", "अगं माय, शांतच बसलोय ना मी! तू जा आता, काळजी नको करू!"),
    ("bob_aarohi_kid", "mr-IN-AarohiNeural", "+3%", "+12Hz", "हो माय, तू जा आता! आम्ही बरोबर पोहोचू!"),
    ("friend_manohar", "mr-IN-ManoharNeural", "+0%", "+6Hz", "अजी काकू, तुम्ही टेन्शन नको घेवा! मी हाय ना याच्या सोबत!")
]

async def test_all():
    os.makedirs("output/voice_benchmark", exist_ok=True)
    for name, voice, rate, pitch, text in lines:
        out_mp3 = f"output/voice_benchmark/{name}.mp3"
        comm = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
        await comm.save(out_mp3)
        print(f"Generated {name} ({voice}, rate={rate}, pitch={pitch})")

asyncio.run(test_all())
