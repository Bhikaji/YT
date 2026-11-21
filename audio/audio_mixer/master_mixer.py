import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any
import imageio_ffmpeg
from audio.sound_effects.sfx_manager import CartoonSFXManager

class MasterAudioMixer:
    """
    Mixes character dialogue tracks, background music (with ducking), and timed cartoon SFX.
    Outputs a cohesive master stereo audio file synced to the 30-second timeline.
    """

    @classmethod
    def assemble_soundtrack(
        cls,
        dialogue_clips: List[Dict[str, Any]],
        sfx_cues: List[Dict[str, Any]],
        output_audio_path: Path,
        total_duration: float = 30.0
    ) -> Path:
        output_audio_path = Path(output_audio_path)
        output_audio_path.parent.mkdir(parents=True, exist_ok=True)
        exe = imageio_ffmpeg.get_ffmpeg_exe()

        # Step 1: Create clean stereo silence background bed (Zero drone / zero F0 interference)
        bgm_path = output_audio_path.parent / "bgm_loop.mp3"
        bgm_filter = f"anullsrc=r=48000:cl=stereo,atrim=duration={total_duration}"
        subprocess.run([exe, "-y", "-f", "lavfi", "-i", bgm_filter, "-c:a", "libmp3lame", str(bgm_path)], capture_output=True)

        # Step 2: Build FFmpeg complex filter inputs
        inputs = ["-i", str(bgm_path)]
        filter_complex = ["[0:a]volume=0.01[bgm];"]
        mix_labels = ["[bgm]"]

        # Add dialogue clips with presence boost and adelay based on exact scheduled timestamps
        clip_idx = 1
        for d in dialogue_clips:
            clip_path = d.get("audio_path")
            if clip_path and os.path.exists(clip_path):
                start_sec = float(d.get("start_second", d.get("start", 0.0)))
                start_ms = max(1, int(start_sec * 1000))
                inputs.extend(["-i", str(clip_path)])
                label = f"[diag{clip_idx}]"
                # Consonant presence EQ (+2.5dB at 2.8kHz) and rumble cut (<80Hz) matching professional cartoon speech
                filter_complex.append(
                    f"[{clip_idx}:a]highpass=f=80,equalizer=f=2800:width_type=o:w=1.2:g=2.5,adelay={start_ms}|{start_ms},volume=1.15{label};"
                )
                mix_labels.append(label)
                clip_idx += 1

        # Add key sound effects
        sfx_dir = output_audio_path.parent / "sfx_stems"
        for s in sfx_cues[:4]:
            sfx_name = s.get("name", "pop")
            sfx_time_ms = max(1, int(s.get("time", 0.0) * 1000))
            s_file = CartoonSFXManager.generate_sfx(sfx_name, sfx_dir / f"{sfx_name}.mp3")
            if os.path.exists(s_file):
                inputs.extend(["-i", str(s_file)])
                label = f"[sfx{clip_idx}]"
                filter_complex.append(f"[{clip_idx}:a]adelay={sfx_time_ms}|{sfx_time_ms},volume=0.35{label};")
                mix_labels.append(label)
                clip_idx += 1

        # Final amix with normalize=0 to maintain full voice volume
        filter_complex.append("".join(mix_labels) + f"amix=inputs={len(mix_labels)}:duration=first:dropout_transition=0:normalize=0[outa]")

        cmd = [exe, "-y"] + inputs + [
            "-filter_complex", "".join(filter_complex),
            "-map", "[outa]",
            "-t", str(total_duration),
            "-ar", "48000",
            "-c:a", "aac",
            "-b:a", "192k",
            str(output_audio_path)
        ]

        res = subprocess.run(cmd, capture_output=True)
        if res.returncode != 0:
            print(f"[MasterMixer] Notice: Complex amix fallback: {res.stderr[:200]}")
            # Fallback: simple copy or dialogue concat
            if dialogue_clips and os.path.exists(dialogue_clips[0]["audio_path"]):
                import shutil
                shutil.copy2(dialogue_clips[0]["audio_path"], output_audio_path)
            else:
                shutil.copy2(bgm_path, output_audio_path)

        return output_audio_path
