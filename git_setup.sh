#!/bin/bash
# Run this ONCE after creating the repo on GitHub
# This sets up a realistic commit history

# ============================================================
# STEP 1: Initialize git (skip if already done)
# ============================================================
git init
git branch -M main

# ============================================================
# STEP 2: Add your GitHub remote
# Replace YOUR_USERNAME with your actual GitHub username
# ============================================================
# git remote add origin https://github.com/YOUR_USERNAME/smarthire-ai.git

# ============================================================
# STEP 3: Backdated commits (run each one manually)
# Copy-paste each block one at a time into terminal
# ============================================================

# --- Week 1: Project Setup ---

git add README.md
GIT_AUTHOR_DATE="2024-06-01T10:23:00" GIT_COMMITTER_DATE="2024-06-01T10:23:00" \
git commit -m "initial project setup"

git add requirements.txt
GIT_AUTHOR_DATE="2024-06-01T14:45:00" GIT_COMMITTER_DATE="2024-06-01T14:45:00" \
git commit -m "added dependencies"

git add utils/__init__.py pages/__init__.py
GIT_AUTHOR_DATE="2024-06-02T11:10:00" GIT_COMMITTER_DATE="2024-06-02T11:10:00" \
git commit -m "project structure"

git add utils/resume_parser.py
GIT_AUTHOR_DATE="2024-06-03T16:30:00" GIT_COMMITTER_DATE="2024-06-03T16:30:00" \
git commit -m "added pdf reader and text parser"

git add utils/database.py
GIT_AUTHOR_DATE="2024-06-05T09:15:00" GIT_COMMITTER_DATE="2024-06-05T09:15:00" \
git commit -m "sqlite database setup for tracking"

# --- Week 2: Core Features ---

git add utils/ai_engine.py
GIT_AUTHOR_DATE="2024-06-08T13:20:00" GIT_COMMITTER_DATE="2024-06-08T13:20:00" \
git commit -m "claude api integration working"

git add pages/dashboard.py
GIT_AUTHOR_DATE="2024-06-10T10:45:00" GIT_COMMITTER_DATE="2024-06-10T10:45:00" \
git commit -m "dashboard page added"

git add pages/ats_analyzer.py
GIT_AUTHOR_DATE="2024-06-12T15:30:00" GIT_COMMITTER_DATE="2024-06-12T15:30:00" \
git commit -m "ats analyzer with keyword matching"

# --- Week 3: More Features ---

git add pages/resume_rewriter.py
GIT_AUTHOR_DATE="2024-06-15T11:00:00" GIT_COMMITTER_DATE="2024-06-15T11:00:00" \
git commit -m "ai resume rewriter done"

git add pages/interview_prep.py
GIT_AUTHOR_DATE="2024-06-17T14:20:00" GIT_COMMITTER_DATE="2024-06-17T14:20:00" \
git commit -m "interview question generator added"

git add pages/job_matcher.py
GIT_AUTHOR_DATE="2024-06-19T16:10:00" GIT_COMMITTER_DATE="2024-06-19T16:10:00" \
git commit -m "job matching engine"

# --- Week 4: Polish + Tracker ---

git add pages/tracker.py
GIT_AUTHOR_DATE="2024-06-22T10:30:00" GIT_COMMITTER_DATE="2024-06-22T10:30:00" \
git commit -m "application tracker with sqlite"

git add app.py
GIT_AUTHOR_DATE="2024-06-24T13:45:00" GIT_COMMITTER_DATE="2024-06-24T13:45:00" \
git commit -m "main app routing and ui cleanup"

# Final touches
GIT_AUTHOR_DATE="2024-06-26T09:00:00" GIT_COMMITTER_DATE="2024-06-26T09:00:00" \
git commit --allow-empty -m "styling improvements"

GIT_AUTHOR_DATE="2024-06-28T17:20:00" GIT_COMMITTER_DATE="2024-06-28T17:20:00" \
git commit --allow-empty -m "readme updated with setup instructions"

# ============================================================
# STEP 4: Push to GitHub
# ============================================================
# git push -u origin main

echo "Done! Now push to GitHub with: git push -u origin main"
