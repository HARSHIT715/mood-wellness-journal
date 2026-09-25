# Mood & Wellness Journal

A small dynamic Flask web application for recording daily mood and journal notes. The project demonstrates Git workflow, automated linting/tests, Docker, GitHub Actions CI/CD, and Render deployment.

## Features
- Add a daily journal entry with name, date, mood (1–5), and note.
- Server-side validation for required fields, date, and mood range.
- Server-calculated average mood.
- Mood emoji indicator.
- JSON API at `/api/entries`.
- Health check at `/health`.
- Footer displays the current deployment commit identifier.

## Tech stack
Python 3.12, Flask, Jinja2, pytest, flake8, Docker, GitHub Actions, Render.

## Run locally
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Test and lint
```powershell
pytest -v
flake8 .
```

## Docker
```powershell
docker build -t mood-wellness-journal .
docker run --rm -p 5000:5000 mood-wellness-journal
```

## CI/CD
Every push and pull request targeting `main` runs linting and tests. A successful test job allows Docker build and `/health` smoke testing. A successful build on `main` triggers the Render deploy hook stored in the GitHub secret `RENDER_DEPLOY_HOOK`.

For the assessment, demonstrate both a deliberately failing branch run and a corrected green run.

## Main routes
| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Dynamic journal homepage |
| `/add` | POST | Validate and add an entry |
| `/api/entries` | GET | JSON data endpoint |
| `/health` | GET | Health check |

## Project structure
```text
mood-wellness-journal/
├── .github/workflows/ci-cd.yml
├── templates/index.html
├── static/style.css
├── app.py
├── test_app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Important deployment note
Create a Render Web Service from the public GitHub repository, choose Docker, set the health check path to `/health`, and turn Render Auto-Deploy off if GitHub Actions is being used to trigger deployment. Add the Render deploy hook as the GitHub Actions secret `RENDER_DEPLOY_HOOK`.

## Academic note
This implementation is intentionally distinct from a generic feedback portal: it uses journal-specific fields, mood scoring, emoji classification, average mood calculation, a wellness-oriented interface, and its own tests and CI/CD workflow.
