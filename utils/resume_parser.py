import re
from typing import Optional


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from uploaded PDF file"""
    try:
        import pdfplumber
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except ImportError:
        # Fallback to PyPDF2
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def extract_keywords(text: str) -> list:
    """Extract technical keywords from text"""
    # Common tech keywords to look for
    tech_keywords = [
        # Languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
        'swift', 'kotlin', 'sql', 'r', 'scala', 'ruby', 'php',
        # Frameworks
        'react', 'angular', 'vue', 'django', 'flask', 'fastapi', 'spring',
        'node.js', 'express', 'tensorflow', 'pytorch', 'keras', 'scikit-learn',
        'pandas', 'numpy', 'streamlit',
        # Cloud
        'aws', 'gcp', 'azure', 'ec2', 's3', 'lambda', 'rds', 'dynamodb',
        'cloudwatch', 'terraform', 'kubernetes', 'docker',
        # Databases
        'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
        # Tools
        'git', 'github', 'jenkins', 'ci/cd', 'ansible', 'kafka',
        # Concepts
        'machine learning', 'deep learning', 'nlp', 'computer vision',
        'microservices', 'rest api', 'graphql', 'agile', 'devops',
        'data structures', 'algorithms', 'system design',
    ]

    text_lower = text.lower()
    found = []
    for keyword in tech_keywords:
        if keyword in text_lower:
            found.append(keyword)

    return list(set(found))


def clean_text(text: str) -> str:
    """Clean and normalize text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special chars except basic punctuation
    text = re.sub(r'[^\w\s.,;:\-@/()•\n]', '', text)
    return text.strip()


def estimate_experience_years(text: str) -> int:
    """Roughly estimate years of experience from resume text"""
    # Look for year patterns
    years = re.findall(r'20\d{2}', text)
    if len(years) >= 2:
        years_int = [int(y) for y in years]
        return max(years_int) - min(years_int)
    return 0


def get_score_color(score: int) -> str:
    """Return color based on score"""
    if score >= 75:
        return "#4ade80"  # green
    elif score >= 50:
        return "#fbbf24"  # yellow
    else:
        return "#f87171"  # red


def get_score_label(score: int) -> str:
    """Return label based on score"""
    if score >= 80:
        return "Excellent"
    elif score >= 65:
        return "Good"
    elif score >= 50:
        return "Average"
    elif score >= 35:
        return "Below Average"
    else:
        return "Poor"


def format_resume_display(text: str) -> str:
    """Format resume text for display"""
    lines = text.split('\n')
    formatted = []
    for line in lines:
        line = line.strip()
        if line:
            formatted.append(line)
    return '\n'.join(formatted)
