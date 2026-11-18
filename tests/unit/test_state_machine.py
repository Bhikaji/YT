import asyncio
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.orchestrator.state_machine import ProductionJobStateMachine, JobState

async def test_job_state_machine_lifecycle():
    print("--- Testing Production Job State Machine ---")
    
    # 1. Create a Job
    job = await ProductionJobStateMachine.create_job(episode_id="ep_test_001")
    job_id = job["job_id"]
    assert job["state"] == JobState.QUEUED.value
    print(f"✔ Job created in state: {job['state']}")

    # 2. Legal transition: QUEUED -> PLANNING
    success = await ProductionJobStateMachine.transition(job_id, JobState.PLANNING)
    assert success
    print("✔ Transitioned: QUEUED -> PLANNING")

    # 3. Legal transition: PLANNING -> SCRIPTING
    success = await ProductionJobStateMachine.transition(job_id, JobState.SCRIPTING)
    assert success
    print("✔ Transitioned: PLANNING -> SCRIPTING")

    # 4. Illegal transition test: SCRIPTING -> PUBLISHED (must raise ValueError)
    try:
        await ProductionJobStateMachine.transition(job_id, JobState.PUBLISHED)
        assert False, "Should have blocked illegal transition!"
    except ValueError as e:
        print(f"✔ Successfully blocked illegal transition: {e}")

    # 5. Recovery transition: Fail and Recover
    await ProductionJobStateMachine.transition(job_id, JobState.FAILED, {"error": "Simulated render abort"})
    print("✔ Transitioned: SCRIPTING -> FAILED (with error payload)")

    await ProductionJobStateMachine.transition(job_id, JobState.RECOVERY, {"action": "Re-queueing scene"})
    print("✔ Transitioned: FAILED -> RECOVERY (Autonomous self-correction)")

    print("\n✔ State Machine Acceptance Test Passed!")

if __name__ == "__main__":
    asyncio.run(test_job_state_machine_lifecycle())
