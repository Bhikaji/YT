import unittest
from pathlib import Path
from audio.voice_generation.speech_intelligence import (
    RegionalDialectIntelligenceEngine,
    SpeechGenerationIntegrityEngine,
    DialogueRepairEngine
)
from audio.dialogue_coordination.speech_validator import SpeechRecognitionValidator

class TestSpeechIntelligence(unittest.TestCase):

    def test_regional_dialect_normalization(self):
        raw = "बहिणमाय मी फक्त फिरावाले चाललो आई, कोणता युद्ध लढाले नाही! आता पैसे देऊन दे तिकिटीचे!"
        spoken = RegionalDialectIntelligenceEngine.normalize_for_speech(raw)
        self.assertIn("बैन माय", spoken)
        self.assertIn("फिरायला", spoken)
        self.assertIn("लढायला", spoken)
        self.assertIn("तिकिटाचे", spoken)
        self.assertNotIn("बहिणमाय", spoken)

    def test_rate_integrity_clamping(self):
        self.assertEqual(SpeechGenerationIntegrityEngine.enforce_rate_integrity("+15%"), "+2%")
        self.assertEqual(SpeechGenerationIntegrityEngine.enforce_rate_integrity("-10%"), "-3%")
        self.assertEqual(SpeechGenerationIntegrityEngine.enforce_rate_integrity("+1%"), "+1%")
        self.assertEqual(SpeechGenerationIntegrityEngine.enforce_rate_integrity("+0%"), "+0%")

    def test_dialogue_repair_engine(self):
        orig = "आई पैसे दे तिकिटाचे"
        repaired = DialogueRepairEngine.repair_line(orig, ["पैसे"])
        self.assertIn(", पैसे", repaired)

if __name__ == "__main__":
    unittest.main()
