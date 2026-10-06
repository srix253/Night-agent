from datetime import datetime

from .controlm import MockControlM
from .decision_engine import DecisionEngine
from .models import Incident, JobStatus
from .pagerduty import MockPagerDuty
from .servicenow import MockServiceNow
from .winscp import MockWinSCP


class NightAgent:
    def __init__(
        self,
        controlm: MockControlM,
        servicenow: MockServiceNow,
        pagerduty: MockPagerDuty,
        winscp: MockWinSCP,
        decision_engine: DecisionEngine,
    ):
        self.controlm = controlm
        self.servicenow = servicenow
        self.pagerduty = pagerduty
        self.winscp = winscp
        self.decision_engine = decision_engine

    def process(self, incident: Incident, now: datetime) -> str:
        job = self.controlm.get_job(incident.job_name)
        decision = self.decision_engine.evaluate(job, now)

        print(
            f"\n[Agent] incident={incident.number} "
            f"job={job.name} status={job.status.value} decision={decision}"
        )

        if decision == "WAIT_MONITOR":
            self.servicenow.update_incident(
                incident,
                f"Control-M job {job.name} is WAIT. "
                f"Expected start: {job.estimated_start_at}. Monitoring continues.",
            )

        elif decision == "WAIT_ETA_EXCEEDED":
            self.servicenow.update_incident(
                incident,
                f"Control-M job {job.name} remains WAIT beyond estimated start "
                f"{job.estimated_start_at}.",
            )
            self.pagerduty.escalate(
                incident.number, "Job remained WAIT beyond estimated start time"
            )

        elif decision == "EXECUTING_MONITOR":
            self.servicenow.update_incident(
                incident,
                f"Control-M job {job.name} is EXECUTING. "
                f"Estimated completion: {job.estimated_completion_at}.",
            )

        elif decision == "EXECUTION_ETA_EXCEEDED":
            self.servicenow.update_incident(
                incident,
                f"Control-M job {job.name} is EXECUTING beyond estimated "
                f"completion {job.estimated_completion_at}.",
            )
            self.pagerduty.escalate(
                incident.number, "Execution exceeded estimated completion time"
            )

        elif decision in {"RETRY", "ESCALATE_FAILURE"}:
            log = self.winscp.get_job_log(job)
            self.servicenow.update_incident(
                incident,
                f"Job ended NOT OK. Error code={job.error_code}; "
                f"message={job.error_message}; log excerpt={log}",
            )

            if decision == "RETRY":
                self.servicenow.update_incident(
                    incident,
                    f"Error {job.error_code} is approved for simulated retry. "
                    f"Retry count before action: {job.retry_count}.",
                )
                retried = self.controlm.rerun_job(job.name)
                self.servicenow.update_incident(
                    incident,
                    f"Simulated retry started. New status={retried.status.value}.",
                )
            else:
                self.pagerduty.escalate(
                    incident.number,
                    f"Non-retryable job failure: {job.error_code}",
                )

        elif decision == "SUCCESS":
            self.servicenow.resolve_incident(
                incident,
                f"Control-M job {job.name} completed successfully.",
            )

        else:
            self.pagerduty.escalate(
                incident.number, "Unknown or unsupported job state"
            )

        return decision
