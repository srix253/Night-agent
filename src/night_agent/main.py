from datetime import datetime

from .agent import NightAgent
from .controlm import MockControlM
from .decision_engine import DecisionEngine
from .models import Incident, Job, JobStatus
from .pagerduty import MockPagerDuty
from .servicenow import MockServiceNow
from .winscp import MockWinSCP


def build_agent(job: Job) -> NightAgent:
    return NightAgent(
        controlm=MockControlM(job),
        servicenow=MockServiceNow(),
        pagerduty=MockPagerDuty(),
        winscp=MockWinSCP(),
        decision_engine=DecisionEngine(
            eta_grace_minutes=15,
            retryable_errors={"CONNECTION_TIMEOUT", "TEMPORARY_NETWORK_ERROR"},
        ),
    )


def run_scenarios() -> None:
    print("=== NIGHT AGENT SIMULATION ===")
    print("Production integrations are DISABLED.\n")

    scenarios = [
        (
            "INC1001",
            Job(
                name="PAYMENT_JOB",
                status=JobStatus.WAIT,
                estimated_start_at=datetime(2026, 10, 6, 23, 30),
            ),
            datetime(2026, 10, 6, 23, 15),
        ),
        (
            "INC1002",
            Job(
                name="REPORT_JOB",
                status=JobStatus.EXECUTING,
                started_at=datetime(2026, 10, 6, 22, 0),
                estimated_completion_at=datetime(2026, 10, 6, 23, 30),
            ),
            datetime(2026, 10, 6, 23, 50),
        ),
        (
            "INC1003",
            Job(
                name="BATCH_JOB",
                status=JobStatus.ENDED_NOT_OK,
                error_code="CONNECTION_TIMEOUT",
                error_message="Database connection timed out",
                log_text="ERROR CONNECTION_TIMEOUT database host did not respond",
            ),
            datetime(2026, 10, 6, 23, 40),
        ),
        (
            "INC1004",
            Job(
                name="CUSTOMER_JOB",
                status=JobStatus.ENDED_NOT_OK,
                error_code="DATA_VALIDATION_ERROR",
                error_message="Invalid customer data",
                log_text="ERROR DATA_VALIDATION_ERROR record 1842 failed validation",
            ),
            datetime(2026, 10, 6, 23, 45),
        ),
        (
            "INC1005",
            Job(
                name="SUCCESS_JOB",
                status=JobStatus.ENDED_OK,
            ),
            datetime(2026, 10, 6, 23, 50),
        ),
    ]

    for incident_number, job, now in scenarios:
        incident = Incident(
            number=incident_number,
            job_name=job.name,
        )
        agent = build_agent(job)
        agent.process(incident, now)

    print("\n=== SIMULATION COMPLETE ===")


if __name__ == "__main__":
    run_scenarios()
