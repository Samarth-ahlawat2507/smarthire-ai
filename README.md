# SmartHire AI ⚡

An AI-powered job application assistant that helps you optimize your resume, prep for interviews, and track your applications — all in one place.

Built because I was spending 3+ hours daily manually tailoring resumes for different companies. Now it takes 15 minutes.

## What it does

**ATS Analyzer** — Upload your resume + paste any job description. Get an instant compatibility score with breakdown of matched/missing keywords, strengths, weaknesses, and quick fixes.

**Resume Rewriter** — One click and the AI rewrites your entire resume specifically for that job. Keeps it human-sounding, ATS-optimized, and tailored to the exact role.

**Interview Prep** — Predicts the exact questions you'll face based on your resume and the job description. Covers technical, behavioral (LP), and project questions.

**Job Matcher** — Matches your profile against multiple job openings and ranks them by compatibility score.

**Application Tracker** — Track every application with status updates, ATS scores, salary ranges, and notes.

## Tech stack

- Python 3.10+
- Streamlit (UI)
- Claude API / Anthropic (AI engine)
- SQLite (application tracking database)
- pdfplumber (resume PDF parsing)

## Setup

```bash
git clone https://github.com/yourusername/smarthire-ai
cd smarthire-ai
pip install -r requirements.txt
```

Set your API key:
```bash
export ANTHROPIC_API_KEY=your_key_here
```

Run:
```bash
streamlit run app.py
```

## Why I built this

75% of resumes get rejected by ATS systems before a human ever sees them. The fix is simple — match your resume keywords to the job description. But doing this manually for 30+ applications is painful.

SmartHire automates the entire process. Analyze, rewrite, prep, track. Done.

## Project structure

```
smarthire/
├── app.py                  # Main entry point
├── pages/
│   ├── dashboard.py        # Home dashboard
│   ├── ats_analyzer.py     # ATS score analyzer
│   ├── resume_rewriter.py  # AI resume rewriter
│   ├── job_matcher.py      # Job matching engine
│   ├── interview_prep.py   # Interview question generator
│   └── tracker.py          # Application tracker
├── utils/
│   ├── ai_engine.py        # Claude API integration
│   ├── resume_parser.py    # PDF parsing + text processing
│   └── database.py         # SQLite database operations
└── requirements.txt
```

## Future plans

- LinkedIn job scraper (automated job fetching)
- AWS Lambda for scheduled job alerts
- Email digest of new matching jobs
- Cover letter generator
- Deployed on AWS EC2

---

Built with Python + Claude AI
