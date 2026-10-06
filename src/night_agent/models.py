from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class JobStatus(str, Enum):
    WAIT = "WAIT"
    EXECUTING = "EXECUTING"
    ENDED_OK = "ENDED_OK"
    ENDED_NOT_OK = "ENDED_NOT_OK"


@dataclass
class Job:
    name: str
    status: JobStatus
    started_at: datetime | None = None
    estimated_start_at: datetime | None = None
    estimated_completion_at: datetime | None = None
    ended_at: datetime | None = None
    error_code: str | None = None
    error_message: str | None = None
    retry_count: int = 0
    log_text: str = ""


@dataclass
class Incident:
    number: str
    job_name: str
    state: str = "OPEN"
    work_notes: list[str] = field(default_factory=list)

    def add_note(self, note: str) -> None:
        self.work_notes.append(note)
