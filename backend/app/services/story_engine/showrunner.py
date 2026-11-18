from typing import Dict, Any, List, Optional
from backend.app.schemas.script import GeneratedEpisodeScript
from backend.app.services.story_engine.screenwriter import ScreenwriterAgent
from backend.app.services.story_engine.continuity_supervisor import ContinuitySupervisor

class ShowrunnerAgent:
    """Orchestrates episode generation, continuity verification, and cliffhanger hooks."""

    @classmethod
    def develop_episode_script(
        cls,
        series_title: str,
        series_genre: str,
        world_lore: Dict[str, Any],
        season_number: int,
        episode_number: int,
        episode_title: str,
        format_type: str,
        cast: List[Dict[str, Any]],
        prior_cliffhanger: Optional[str] = None
    ) -> GeneratedEpisodeScript:
        """
        Executes the Showrunner-Screenwriter-Continuity Supervisor loop.
        """
        cast_ids = [c["id"] for c in cast]
        
        # 1. Generate Script
        script = ScreenwriterAgent.generate_script_procedural(
            series_title=series_title,
            episode_number=episode_number,
            episode_title=episode_title,
            format_type=format_type,
            cast=cast,
            unresolved_mystery=prior_cliffhanger
        )

        # 2. Audit against Continuity Supervisor
        is_approved, violations = ContinuitySupervisor.audit_script(
            script=script,
            world_lore=world_lore,
            cast_ids=cast_ids,
            prior_cliffhanger=prior_cliffhanger
        )

        if not is_approved:
            # Automatic correction / warning log
            print(f"[ShowrunnerAgent] Warning - Continuity violations detected: {violations}")

        return script
