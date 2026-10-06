class MockPagerDuty:
    """Simulation-only PagerDuty adapter."""

    def escalate(self, incident_number: str, reason: str) -> None:
        print(
            f"[PagerDuty] ESCALATION - incident={incident_number} reason={reason}"
        )
