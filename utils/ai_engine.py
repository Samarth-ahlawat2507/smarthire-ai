import anthropic
import json
import re


def get_client():
    """Initialize Claude client"""
    return anthropic.Anthropic()


def analyze_ats_score(resume_text: str, job_description: str) -> dict:
    """
    Analyze resume against job description and return ATS score with details
    """
    client = get_client()

    prompt = f"""You are an expert ATS (Applicant Tracking System) analyzer with deep knowledge of how companies like Amazon, Google, and Microsoft screen resumes.

Analyze this resume against the job description and provide a detailed ATS compatibility report.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY a valid JSON object with this exact structure:
{{
    "overall_score": <integer 0-100>,
    "keyword_score": <integer 0-100>,
    "skills_score": <integer 0-100>,
    "experience_score": <integer 0-100>,
    "format_score": <integer 0-100>,
    "matched_keywords": ["keyword1", "keyword2", ...],
    "missing_keywords": ["keyword1", "keyword2", ...],
    "matched_skills": ["skill1", "skill2", ...],
    "missing_skills": ["skill1", "skill2", ...],
    "strengths": ["strength1", "strength2", "strength3"],
    "weaknesses": ["weakness1", "weakness2", "weakness3"],
    "quick_fixes": ["fix1", "fix2", "fix3", "fix4"],
    "verdict": "<one sentence overall assessment>"
}}

Be realistic and accurate. Most resumes score between 40-75 unless very well tailored."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text.strip()
    # Clean JSON
    text = re.sub(r'```json\n?', '', text)
    text = re.sub(r'```\n?', '', text)
    return json.loads(text)


def rewrite_resume(resume_text: str, job_description: str, tone: str = "professional") -> dict:
    """
    Rewrite resume optimized for a specific job description
    """
    client = get_client()

    prompt = f"""You are an expert resume writer who has helped 10,000+ candidates land jobs at top tech companies including Amazon, Google, Microsoft, and Flipkart.

Rewrite this resume to be perfectly optimized for the job description below. Make it ATS-friendly while keeping it authentic and human-sounding.

ORIGINAL RESUME:
{resume_text}

TARGET JOB DESCRIPTION:
{job_description}

TONE: {tone}

Rules:
1. Use strong action verbs (built, designed, implemented, reduced, improved, led, etc.)
2. Add quantifiable metrics where possible (%, numbers, scale)
3. Mirror keywords from the job description naturally
4. Keep bullet points concise (1-2 lines max)
5. Make it sound like a human wrote it, not AI
6. Preserve all real information, only enhance presentation

Return ONLY a valid JSON object:
{{
    "rewritten_resume": "<full rewritten resume as plain text>",
    "key_changes": ["change1", "change2", "change3", "change4", "change5"],
    "keywords_added": ["keyword1", "keyword2", "keyword3"],
    "estimated_score_improvement": <integer, how many points ATS score likely improved>,
    "tips": ["tip1", "tip2", "tip3"]
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text.strip()
    text = re.sub(r'```json\n?', '', text)
    text = re.sub(r'```\n?', '', text)
    return json.loads(text)


def generate_interview_questions(resume_text: str, job_description: str, company: str = "Amazon") -> dict:
    """
    Generate likely interview questions based on resume and job description
    """
    client = get_client()

    prompt = f"""You are a senior interviewer at {company} with 10+ years of experience hiring SDE candidates.

Based on this resume and job description, generate the most likely interview questions this candidate will face.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

COMPANY: {company}

Return ONLY a valid JSON object:
{{
    "technical_questions": [
        {{"question": "...", "why_asked": "...", "hint": "..."}},
        {{"question": "...", "why_asked": "...", "hint": "..."}},
        {{"question": "...", "why_asked": "...", "hint": "..."}},
        {{"question": "...", "why_asked": "...", "hint": "..."}},
        {{"question": "...", "why_asked": "...", "hint": "..."}}
    ],
    "behavioral_questions": [
        {{"question": "...", "lp": "Leadership Principle this tests", "star_hint": "..."}},
        {{"question": "...", "lp": "...", "star_hint": "..."}},
        {{"question": "...", "lp": "...", "star_hint": "..."}},
        {{"question": "...", "lp": "...", "star_hint": "..."}},
        {{"question": "...", "lp": "...", "star_hint": "..."}}
    ],
    "project_questions": [
        {{"question": "...", "what_they_want": "..."}},
        {{"question": "...", "what_they_want": "..."}},
        {{"question": "...", "what_they_want": "..."}}
    ],
    "dsa_topics": ["topic1", "topic2", "topic3", "topic4"],
    "preparation_tips": ["tip1", "tip2", "tip3"]
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text.strip()
    text = re.sub(r'```json\n?', '', text)
    text = re.sub(r'```\n?', '', text)
    return json.loads(text)


def match_jobs(resume_text: str, jobs: list) -> list:
    """
    Match resume against a list of jobs and score each
    """
    client = get_client()

    jobs_text = "\n\n".join([
        f"JOB {i+1}: {job['title']} at {job['company']}\n{job['description'][:300]}..."
        for i, job in enumerate(jobs)
    ])

    prompt = f"""You are an expert job matching system. Score each job against this resume.

RESUME:
{resume_text}

JOBS TO EVALUATE:
{jobs_text}

Return ONLY a valid JSON array:
[
    {{"job_index": 0, "match_score": <0-100>, "match_reason": "...", "missing": ["skill1", "skill2"]}},
    ...
]
One object per job in same order."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text.strip()
    text = re.sub(r'```json\n?', '', text)
    text = re.sub(r'```\n?', '', text)
    return json.loads(text)
