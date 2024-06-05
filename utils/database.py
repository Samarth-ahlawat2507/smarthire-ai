import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "applications.db"


def init_db():
    """Initialize SQLite database"""
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT DEFAULT 'Applied',
            ats_score INTEGER DEFAULT 0,
            applied_date TEXT,
            last_updated TEXT,
            notes TEXT,
            job_url TEXT,
            salary_range TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            company TEXT,
            role TEXT,
            ats_score INTEGER,
            keywords_matched INTEGER,
            keywords_missing INTEGER
        )
    """)

    conn.commit()
    conn.close()


def add_application(company: str, role: str, ats_score: int = 0,
                    job_url: str = "", salary_range: str = "", notes: str = "") -> int:
    """Add new job application"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("""
        INSERT INTO applications (company, role, status, ats_score, applied_date, last_updated, notes, job_url, salary_range)
        VALUES (?, ?, 'Applied', ?, ?, ?, ?, ?, ?)
    """, (company, role, ats_score, now, now, notes, job_url, salary_range))

    app_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return app_id


def get_all_applications() -> list:
    """Get all applications"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications ORDER BY applied_date DESC")
    rows = cursor.fetchall()
    conn.close()

    columns = ['id', 'company', 'role', 'status', 'ats_score',
               'applied_date', 'last_updated', 'notes', 'job_url', 'salary_range']
    return [dict(zip(columns, row)) for row in rows]


def update_application_status(app_id: int, status: str):
    """Update application status"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("""
        UPDATE applications SET status = ?, last_updated = ? WHERE id = ?
    """, (status, now, app_id))

    conn.commit()
    conn.close()


def delete_application(app_id: int):
    """Delete an application"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE id = ?", (app_id,))
    conn.commit()
    conn.close()


def get_stats() -> dict:
    """Get application statistics"""
    init_db()
    apps = get_all_applications()

    if not apps:
        return {
            "total": 0, "applied": 0, "interviewing": 0,
            "offered": 0, "rejected": 0, "avg_ats": 0
        }

    stats = {
        "total": len(apps),
        "applied": sum(1 for a in apps if a['status'] == 'Applied'),
        "interviewing": sum(1 for a in apps if a['status'] == 'Interviewing'),
        "offered": sum(1 for a in apps if a['status'] == 'Offer Received'),
        "rejected": sum(1 for a in apps if a['status'] == 'Rejected'),
        "avg_ats": int(sum(a['ats_score'] for a in apps) / len(apps)) if apps else 0
    }
    return stats


def log_analysis(company: str, role: str, ats_score: int,
                 keywords_matched: int, keywords_missing: int):
    """Log an ATS analysis"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("""
        INSERT INTO analyses (timestamp, company, role, ats_score, keywords_matched, keywords_missing)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (now, company, role, ats_score, keywords_matched, keywords_missing))

    conn.commit()
    conn.close()
