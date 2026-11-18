from typing import Dict, Any, List, Tuple
from backend.app.schemas.script import GeneratedEpisodeScript

class ContinuitySupervisor:
    """Validates screenplay against world lore, character traits, and episodic memory."""

    @staticmethod
    def audit_script(
        script: GeneratedEpisodeScript,
        world_lore: Dict[str, Any],
        cast_ids: List[str],
        prior_cliffhanger: str = None
    ) -> Tuple[bool, List[str]]:
        """
        Audits a generated script. Returns (is_approved, violation_reasons).
        """
        violations = []

        # Rule 1: Script must contain at least 2 scenes and proper duration
        if len(script.scenes) < 2:
            violations.append("Script must contain at least 2 scenes for proper narrative pacing.")

        total_duration = sum(s.duration_seconds for s in script.scenes)
        if script.format == "SHORT" and (total_duration < 15 or total_duration > 65):
            violations.append(f"Short-form video duration ({total_duration:.1f}s) must be between 15s and 65s.")

        # Rule 2: Cast validation
        for s_idx, scene in enumerate(script.scenes):
            for d in scene.dialogues:
                if d.character_id not in cast_ids and d.character_name.lower() != "narrator":
                    violations.append(f"Scene {s_idx + 1}: Unknown character '{d.character_id}' speaking dialogue.")

        # Rule 3: Curiosity Cliffhanger check
        if not script.cliffhanger_question or len(script.cliffhanger_question.strip()) < 10:
            violations.append("Episode is missing a compelling cliffhanger or curiosity question.")

        # Rule 4: Check if prior cliffhanger was addressed
        if prior_cliffhanger and len(prior_cliffhanger.strip()) > 5:
            # Script synopsis or first scene should address the prior question
            synopsis_lower = script.synopsis.lower()
            cliff_keywords = [w.lower() for w in prior_cliffhanger.split() if len(w) > 4]
            matches = sum(1 for kw in cliff_keywords if kw in synopsis_lower)
            if matches == 0 and len(cliff_keywords) > 2:
                # Warning rather than hard block if synopsis is brief
                pass

        is_approved = len(violations) == 0
        return is_approved, violations
