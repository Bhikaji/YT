import math
from typing import Dict, Any, List, Optional
from animation.lip_sync.phoneme_mapper import PhonemeMapper

class SpeechSynchronizer:
    """
    Coordinates dialogue timing, phoneme transitions, and multi-character turn-taking.
    Ensures characters speak only during their dialogue timestamps with realistic, fluid lip sync.
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
        Matches actual synthesized audio timestamps with dynamic syllable transitions.
        """
        for d in dialogues:
            if d.get("speaker_id") == character_id:
                start = float(d.get("start_second", 0.0))
                end = float(d.get("end_second", 0.0))
                if start <= t_sec <= end:
                    elapsed = t_sec - start
                    # Conversational cadence: 5.5 to 6.2 syllable transitions per second
                    speech_speed = 5.8
                    phase = elapsed * speech_speed * 2.0 * math.pi
                    oscillation = (math.sin(phase) + 1.0) / 2.0  # 0.0 to 1.0

                    emotion = d.get("emotion", "curious")

                    # High-energy shocked / screaming dialogue articulates expressively
                    if emotion in ["shocked", "fearful", "screaming"]:
                        if oscillation > 0.45:
                            return PhonemeMapper.get_mouth_for_phoneme("SCREAM")
                        elif oscillation > 0.20:
                            return PhonemeMapper.get_mouth_for_phoneme("A_I")
                        else:
                            return PhonemeMapper.get_mouth_for_phoneme("E")

                    # Natural spoken conversation cadence
                    if oscillation > 0.65:
                        phoneme = "A_I" if (int(t_sec * 5) % 2 == 0) else "O_U"
                    elif oscillation > 0.35:
                        phoneme = "E" if (int(t_sec * 3) % 2 == 0) else "L_TH"
                    elif oscillation > 0.15:
                        phoneme = "F_V"
                    else:
                        phoneme = "M_B_P"

                    return PhonemeMapper.get_mouth_for_phoneme(phoneme)

        # Not speaking -> listening / resting mouth (strictly closed)
        return PhonemeMapper.get_mouth_for_phoneme("REST")
