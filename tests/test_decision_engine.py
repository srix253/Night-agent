import unittest
from datetime import datetime

from src.night_agent.decision_engine import DecisionEngine
from src.night_agent.models import Job, JobStatus


class DecisionEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = DecisionEngine(
            retryable_errors={"CONNECTION_TIMEOUT"}
        )

    def test_wait_within_eta(self):
        job = Job(
            name="JOB",
            status=JobStatus.WAIT,
            estimated_start_at=datetime(2026, 10, 6, 23, 30),
        )
        result = self.engine.evaluate(job, datetime(2026, 10, 6, 23, 15))
        self.assertEqual(result, "WAIT_MONITOR")

    def test_wait_eta_exceeded(self):
        job = Job(
            name="JOB",
            status=JobStatus.WAIT,
            estimated_start_at=datetime(2026, 10, 6, 23, 30),
        )
        result = self.engine.evaluate(job, datetime(2026, 10, 6, 23, 45))
        self.assertEqual(result, "WAIT_ETA_EXCEEDED")

    def test_executing_eta_exceeded(self):
        job = Job(
            name="JOB",
            status=JobStatus.EXECUTING,
            estimated_completion_at=datetime(2026, 10, 6, 23, 30),
        )
        result = self.engine.evaluate(job, datetime(2026, 10, 6, 23, 45))
        self.assertEqual(result, "EXECUTION_ETA_EXCEEDED")

    def test_retryable_failure(self):
        job = Job(
            name="JOB",
            status=JobStatus.ENDED_NOT_OK,
            error_code="CONNECTION_TIMEOUT",
        )
        result = self.engine.evaluate(job, datetime(2026, 10, 6, 23, 45))
        self.assertEqual(result, "RETRY")

    def test_non_retryable_failure(self):
        job = Job(
            name="JOB",
            status=JobStatus.ENDED_NOT_OK,
            error_code="DATA_VALIDATION_ERROR",
        )
        result = self.engine.evaluate(job, datetime(2026, 10, 6, 23, 45))
        self.assertEqual(result, "ESCALATE_FAILURE")

    def test_success(self):
        job = Job(name="JOB", status=JobStatus.ENDED_OK)
        result = self.engine.evaluate(job, datetime(2026, 10, 6, 23, 45))
        self.assertEqual(result, "SUCCESS")


if __name__ == "__main__":
    unittest.main()
