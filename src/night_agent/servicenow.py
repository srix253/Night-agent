from .models import Incident


class MockServiceNow:
    """Simulation-only ServiceNow adapter."""

    def update_incident(self, incident: Incident, note: str) -> None:
        incident.add_note(note)
        print(f"[ServiceNow] {incident.number}: {note}")

    def resolve_incident(self, incident: Incident, note: str) -> None:
        incident.add_note(note)
        incident.state = "RESOLVED"
        print(f"[ServiceNow] {incident.number}: RESOLVED - {note}")
