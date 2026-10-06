from dataclasses import replace

from .models import Job


class MockControlM:
    """Simulation-only Control-M adapter."""

    def __init__(self, job: Job):
        self.job = job

    def get_job(self, job_name: str) -> Job:
        if job_name != self.job.name:
            raise ValueError(f"Unknown simulated job: {job_name}")
        return replace(self.job)

    def rerun_job(self, job_name: str) -> Job:
        if job_name != self.job.name:
            raise ValueError(f"Unknown simulated job: {job_name}")

        self.job.retry_count += 1
        self.job.status = self.job.status.EXECUTING
        return replace(self.job)
