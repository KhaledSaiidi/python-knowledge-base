# Running Python Files

This guide explains how to run Python scripts and APIs inside this project.

---

## 1. Activate virtual environment (required)

`source .venv/bin/activate`

---

## 2. Run a Python file

From the root of the repository:

`python 01_python_basics/variables.py`

or:

`python3 01_python_basics/variables.py`

---

## 3. Create and run a simple file

Create:

`touch 01_python_basics/hello.py`

Content:

`print("Hello Python")`

Run:

`python 01_python_basics/hello.py`

Expected output:

`Hello Python`

---

## 4. Run Python interactively

Start shell:

`python`

Example:

`name = "Khaled"`
`print(name)`

Exit:

`exit()`

---

## 5. Run one-line commands

`python -c 'print("Hello from terminal")'`

---

## 6. Run Flask API

Example:

`python 04_api_basics/simple_get_api.py`

Test API:

`curl http://localhost:3000/health`

---

## 7. Stop a running program

Press:

`CTRL + C`

---

## 8. Common errors

### File not found

Wrong:

`python variables.py`

Correct:

`python 01_python_basics/variables.py`

---

### Virtual environment not active

Fix:

`source .venv/bin/activate`

---

### Missing packages

Fix:

`pip install -r requirements.txt`

---

## 9. Recommended workflow

`cd python-knowledge-base`
`source .venv/bin/activate`

`python 01_python_basics/variables.py`
`python 04_api_basics/simple_get_api.py`

`deactivate`

---

## Key idea

- Each .py file = executable script
- python <file> runs it
- Flask files start a server you can test with curl or browser
