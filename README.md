# Night Agent

A safe, simulation-first prototype for monitoring Control-M jobs and coordinating ServiceNow/PagerDuty actions.

## Current scope

This first version does **not** connect to production systems. It simulates:

- Control-M job status
- ServiceNow incident updates
- PagerDuty escalation
- WinSCP/log retrieval
- Retry decisions
- Night-shift monitoring

The goal is to validate the operational decision flow before adding real integrations.

## Requirements

- Python 3.10+
- Git

## Run locally

Clone the repository:

```bash
git clone https://github.com/srix253/Night-agent.git
cd Night-agent
```

Create a virtual environment:

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the simulation:

```bash
python -m src.night_agent.main
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Simulation scenarios

The default runner demonstrates:

1. WAIT within ETA - continue monitoring.
2. EXECUTING beyond ETA - escalate through PagerDuty.
3. ENDED NOT OK with a retryable error - simulate retry.
4. ENDED NOT OK with a non-retryable error - escalate.
5. Successful job - close/resolve monitoring.

## Safety

The prototype uses mock adapters only. It does not call Control-M, ServiceNow, PagerDuty, WinSCP, or any external production endpoint.

Real integrations should be added only after the decision rules and authorization controls are reviewed.
