from datetime import datetime

from .models import Job, JobStatus


class DecisionEngine:
    """Pure decision logic. No external side effects."""

    def __init__(self, eta_grace_minutes: int = 15, retryable_errors: set[str] | None = None):
        self.eta_grace_minutes = eta_grace_minutes
        self.retryable_errors = retryable_errors or set()

    def evaluate(self, job: Job, now: datetime) -> str:
        if job.status == JobStatus.WAIT:
            if job.estimated_start_at and now > job.estimated_start_at:
                return "WAIT_ETA_EXCEEDED"
            return "WAIT_MONITOR"

        if job.status == JobStatus.EXECUTING:
            if (
                job.estimated_completion_at
                and now > job.estimated_completion_at
            ):
                return "EXECUTION_ETA_EXCEEDED"
            return "EXECUTING_MONITOR"

        if job.status == JobStatus.ENDED_NOT_OK:
            if job.error_code in self.retryable_errors:
                return "RETRY"
            return "ESCALATE_FAILURE"

        if job.status == JobStatus.ENDED_OK:
            return "SUCCESS"

        return "ESCALATE_UNKNOWN"
