from .models import Job


class MockWinSCP:
    """Simulation-only log retrieval adapter."""

    def get_job_log(self, job: Job) -> str:
        print(f"[WinSCP] Retrieving simulated log for {job.name}")
        return job.log_text
