import math
from typing import Dict, Any, List, Optional
from animation.lip_sync.phoneme_mapper import PhonemeMapper

class SpeechSynchronizer:
    """
    Coordinates dialogue timing, phoneme transitions, and multi-character turn-taking.
    Ensures characters speak only during their dialogue timestamps.
    """

    @classmethod
    def get_mouth_state(
        cls,
        character_id: str,
        t_sec: float,
        dialogues: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Determines mouth opening and phoneme shape for a character at time t_sec.
        """
        for d in dialogues:
            if d.get("speaker_id") == character_id:
                start = d.get("start_second", 0.0)
                end = d.get("end_second", 0.0)
                if start <= t_sec <= end:
                    # Speaking cadence: 5 to 7 syllable transitions per second
                    speech_speed = 6.0
                    phase = (t_sec - start) * speech_speed * 2.0 * math.pi
                    oscillation = (math.sin(phase) + 1.0) / 2.0  # 0.0 to 1.0

                    if d.get("emotion") in ["shocked", "fearful", "screaming"]:
                        return PhonemeMapper.get_mouth_for_phoneme("SCREAM")

                    # Alternate between open vowel and closed consonant
                    if oscillation > 0.6:
                        # Open
                        phoneme = "A_I" if (int(t_sec * 4) % 2 == 0) else "O_U"
                    elif oscillation > 0.3:
                        phoneme = "E"
                    else:
                        phoneme = "M_B_P"

                    return PhonemeMapper.get_mouth_for_phoneme(phoneme)

        # Not speaking -> listening / resting mouth
        return PhonemeMapper.get_mouth_for_phoneme("REST")
