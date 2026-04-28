# Python Installation & Environment Setup

This project uses a **virtual environment (venv)** to isolate dependencies and avoid conflicts with system-wide Python packages.

---

## 1. Check Python installation

`python3 --version`

Expected output:

`Python 3.x.x`

If not installed, install Python 3 before continuing.

---

## 2. Create a virtual environment

From the root of the repository:

`python3 -m venv .venv`

### Why this is important
- Creates an isolated Python environment
- Prevents conflicts with global packages
- Ensures reproducibility across machines

---

## 3. Activate the virtual environment

`source .venv/bin/activate`

You should see:

`(.venv)`

### Why activation matters
- Ensures all installed packages go into this project only
- Ensures `python` and `pip` point to the virtual environment

---

## 4. Upgrade pip

`python -m pip install --upgrade pip`

### Why
- Ensures compatibility with modern packages

---

## 5. Create requirements file

`touch requirements.txt`

Add:

`flask`
`requests`

---

## 6. Install dependencies

`pip install -r requirements.txt`

### Why
- Installs all required libraries for this project
- Ensures consistent environment setup

---

## 7. Verify installation

`pip list`

You should see packages such as:

`Flask`
`requests`

---

## 8. Freeze dependencies (important)

`pip freeze > requirements.txt`

### Why
- Saves exact package versions
- Ensures reproducibility across environments (CI/CD, teammates, servers)

---

## 9. Deactivate virtual environment

`deactivate`

### Why
- Exit the isolated environment
- Return to system Python

---

## 10. Daily workflow

Every time you work on this project:

`cd python-knowledge-base`
`source .venv/bin/activate`

Run your code, then:

`deactivate`

---

## Summary

| Step | Purpose |
|------|--------|
| venv creation | Isolated environment |
| activation | Use project-specific Python |
| install requirements | Get dependencies |
| freeze | Lock versions |
| deactivate | Exit environment |

---

## Rule

Always activate the virtual environment before running any Python code in this project.
