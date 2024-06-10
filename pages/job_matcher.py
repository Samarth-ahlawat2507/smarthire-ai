import streamlit as st
from utils.resume_parser import get_score_color


SAMPLE_JOBS = [
    {
        "title": "SDE1 - Backend Engineer",
        "company": "Amazon",
        "location": "Bangalore",
        "salary": "20-32 LPA",
        "type": "Full Time",
        "description": """We are looking for a Software Development Engineer to join our team.
        Requirements: Strong CS fundamentals, proficiency in Python or Java, experience with AWS,
        knowledge of distributed systems, data structures and algorithms, REST APIs,
        microservices architecture. Experience with Docker, Kubernetes is a plus.
        You will work on customer-facing features at massive scale."""
    },
    {
        "title": "Software Engineer - Platform",
        "company": "Flipkart",
        "location": "Bangalore",
        "salary": "15-25 LPA",
        "type": "Full Time",
        "description": """Join Flipkart's platform team building India's largest e-commerce infrastructure.
        Skills needed: Python, Java, distributed systems, Kafka, microservices,
        SQL databases, system design. Experience with cloud platforms AWS or GCP preferred.
        Strong problem solving and DSA skills required."""
    },
    {
        "title": "Backend Developer",
        "company": "Razorpay",
        "location": "Bangalore",
        "salary": "12-20 LPA",
        "type": "Full Time",
        "description": """Build payment infrastructure that powers India's digital economy.
        Requirements: Python or Go, REST APIs, SQL and NoSQL databases, Redis,
        payment systems knowledge a plus. Strong understanding of security,
        data structures, system design. Startup mindset required."""
    },
    {
        "title": "SDE - AI/ML Platform",
        "company": "Adobe",
        "location": "Noida",
        "salary": "15-22 LPA",
        "type": "Full Time",
        "description": """Build AI-powered creative tools used by millions globally.
        Skills: Python, ML frameworks (TensorFlow, PyTorch), cloud platforms,
        REST APIs, strong algorithms and data structures knowledge.
        Experience with model deployment, AWS or GCP, Docker preferred."""
    },
    {
        "title": "Cloud Engineer",
        "company": "Microsoft",
        "location": "Hyderabad",
        "salary": "18-28 LPA",
        "type": "Full Time",
        "description": """Join Azure team building world-class cloud infrastructure.
        Requirements: Strong programming skills in Python or C#, cloud architecture,
        Kubernetes, Terraform, CI/CD pipelines, distributed systems,
        networking fundamentals, system design."""
    },
]


def show():
    st.markdown("""
    <div style='padding: 8px 0 24px 0;'>
        <div style='font-size: 26px; font-weight: 700; color: #fff;'>🔍 Job Matcher</div>
        <div style='font-size: 14px; color: #6b7280; margin-top: 6px;'>
            See how well your resume matches real job openings. Ranked by compatibility score.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("<div style='font-size: 13px; font-weight: 500; color: #9ca3af; margin-bottom: 8px;'>Your Resume</div>",
                    unsafe_allow_html=True)

        default_resume = st.session_state.get('last_resume', '')
        resume_text = st.text_area(
            "Resume",
            value=default_resume,
            height=200,
            label_visibility="collapsed",
            placeholder="Paste your resume to match against jobs..."
        )

    with col2:
        st.markdown("<div style='font-size: 13px; font-weight: 500; color: #9ca3af; margin-bottom: 8px;'>Filters</div>",
                    unsafe_allow_html=True)

        location_filter = st.multiselect(
            "Location",
            ["Bangalore", "Hyderabad", "Noida", "Chennai", "Mumbai", "Gurgaon"],
            default=["Bangalore", "Hyderabad"],
            label_visibility="collapsed"
        )

        min_salary = st.slider("Min salary (LPA)", 5, 50, 10,
                               label_visibility="collapsed")

        company_types = st.multiselect(
            "Company type",
            ["Product", "Startup", "MNC", "Finance"],
            default=["Product", "MNC"],
            label_visibility="collapsed"
        )

    st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)
    match_btn = st.button("🔍 Find Matching Jobs", use_container_width=True)

    # Always show jobs
    st.markdown("<hr style='border-color: #2d2f3e; margin: 16px 0;'>",
                unsafe_allow_html=True)

    if match_btn and resume_text:
        with st.spinner("Matching your profile against job openings..."):
            try:
                from utils.ai_engine import match_jobs
                matches = match_jobs(resume_text, SAMPLE_JOBS)

                # Merge scores with job data
                scored_jobs = []
                for match in matches:
                    idx = match.get('job_index', 0)
                    if idx < len(SAMPLE_JOBS):
                        job = SAMPLE_JOBS[idx].copy()
                        job['match_score'] = match.get('match_score', 0)
                        job['match_reason'] = match.get('match_reason', '')
                        job['missing'] = match.get('missing', [])
                        scored_jobs.append(job)

                scored_jobs.sort(key=lambda x: x['match_score'], reverse=True)
                st.session_state['matched_jobs'] = scored_jobs

            except Exception as e:
                st.error(f"Matching failed: {str(e)}")
                st.session_state['matched_jobs'] = [{**j, 'match_score': 0,
                                                      'match_reason': '', 'missing': []}
                                                     for j in SAMPLE_JOBS]
    else:
        if 'matched_jobs' not in st.session_state:
            st.session_state['matched_jobs'] = [{**j, 'match_score': 0,
                                                  'match_reason': 'Add resume to see match score',
                                                  'missing': []}
                                                 for j in SAMPLE_JOBS]

    # Display jobs
    st.markdown(f"""
    <div style='font-size: 13px; color: #6b7280; margin-bottom: 16px;'>
        Showing {len(st.session_state['matched_jobs'])} jobs
    </div>
    """, unsafe_allow_html=True)

    for job in st.session_state['matched_jobs']:
        score = job.get('match_score', 0)
        color = get_score_color(score) if score > 0 else '#6b7280'

        with st.expander(f"{'🟢' if score >= 70 else '🟡' if score >= 50 else '⚪'} "
                         f"{job['title']} — {job['company']} | {job['salary']}"):

            col_info, col_score = st.columns([3, 1])

            with col_info:
                st.markdown(f"""
                <div style='display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;'>
                    <span class='badge-blue'>📍 {job['location']}</span>
                    <span class='badge-blue'>💼 {job['type']}</span>
                    <span class='badge-green'>💰 {job['salary']}</span>
                </div>
                <div style='font-size: 13px; color: #9ca3af; line-height: 1.6;'>
                    {job['description'][:300]}...
                </div>
                """, unsafe_allow_html=True)

                if job.get('missing'):
                    st.markdown("<div style='margin-top: 12px;'>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div style='font-size: 12px; color: #f87171; margin-bottom: 6px;'>
                        Missing from your resume:
                    </div>
                    """, unsafe_allow_html=True)
                    chips = " ".join([f'<span class="badge-red">{m}</span>'
                                      for m in job['missing'][:5]])
                    st.markdown(f"{chips}</div>", unsafe_allow_html=True)

            with col_score:
                if score > 0:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 16px;'>
                        <div style='font-size: 40px; font-weight: 700;
                                    color: {color};'>{score}%</div>
                        <div style='font-size: 12px; color: #6b7280; margin-top: 4px;'>Match Score</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style='text-align: center; padding: 16px;'>
                        <div style='font-size: 13px; color: #6b7280;'>
                            Add resume<br>to see score
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                if job.get('match_reason'):
                    st.markdown(f"""
                    <div style='font-size: 11px; color: #6b7280; text-align: center;
                                padding: 0 8px;'>{job['match_reason']}</div>
                    """, unsafe_allow_html=True)
