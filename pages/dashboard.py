import streamlit as st
from utils.database import get_stats, get_all_applications


def show():
    # Hero section
    st.markdown("""
    <div style='padding: 32px 0 24px 0;'>
        <div class='hero-title'>
            Your AI-Powered<br>
            <span class='hero-accent'>Placement Assistant</span>
        </div>
        <div class='hero-sub'>
            Analyze your resume, optimize for ATS, prep for interviews,<br>
            and track every application — all in one place.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    stats = get_stats()
    apps = get_all_applications()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Applied", stats['total'])
    with col2:
        st.metric("Interviewing", stats['interviewing'])
    with col3:
        st.metric("Offers", stats['offered'])
    with col4:
        st.metric("Rejected", stats['rejected'])
    with col5:
        st.metric("Avg ATS Score", f"{stats['avg_ats']}%")

    st.markdown("<hr style='border-color: #2d2f3e; margin: 24px 0;'>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("<div class='section-header'>Quick Actions</div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("""
            <div class='sh-card' style='cursor: pointer; border-color: #4f46e5;'>
                <div style='font-size: 28px; margin-bottom: 8px;'>📄</div>
                <div style='font-size: 15px; font-weight: 600; color: #fff;'>Check ATS Score</div>
                <div style='font-size: 13px; color: #6b7280; margin-top: 4px;'>
                    Upload resume + job description.<br>Get instant compatibility score.
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown("""
            <div class='sh-card' style='cursor: pointer;'>
                <div style='font-size: 28px; margin-bottom: 8px;'>✏️</div>
                <div style='font-size: 15px; font-weight: 600; color: #fff;'>Rewrite Resume</div>
                <div style='font-size: 13px; color: #6b7280; margin-top: 4px;'>
                    AI rewrites your resume<br>tailored to the exact job.
                </div>
            </div>
            """, unsafe_allow_html=True)

        c3, c4 = st.columns(2)

        with c3:
            st.markdown("""
            <div class='sh-card'>
                <div style='font-size: 28px; margin-bottom: 8px;'>🎯</div>
                <div style='font-size: 15px; font-weight: 600; color: #fff;'>Interview Prep</div>
                <div style='font-size: 13px; color: #6b7280; margin-top: 4px;'>
                    Get predicted questions<br>based on your resume + JD.
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            st.markdown("""
            <div class='sh-card'>
                <div style='font-size: 28px; margin-bottom: 8px;'>📊</div>
                <div style='font-size: 15px; font-weight: 600; color: #fff;'>Track Applications</div>
                <div style='font-size: 13px; color: #6b7280; margin-top: 4px;'>
                    Log and track every<br>application in one place.
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Recent applications
        if apps:
            st.markdown("<div class='section-header' style='margin-top: 28px;'>Recent Applications</div>",
                        unsafe_allow_html=True)

            for app in apps[:4]:
                status_color = {
                    'Applied': '#fbbf24',
                    'Interviewing': '#60a5fa',
                    'Offer Received': '#4ade80',
                    'Rejected': '#f87171',
                    'Withdrawn': '#6b7280'
                }.get(app['status'], '#6b7280')

                st.markdown(f"""
                <div class='sh-card' style='padding: 16px 20px; margin-bottom: 8px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <div style='font-size: 14px; font-weight: 600; color: #fff;'>
                                {app['role']}
                            </div>
                            <div style='font-size: 12px; color: #6b7280; margin-top: 2px;'>
                                {app['company']} · {app['applied_date']}
                            </div>
                        </div>
                        <div style='display: flex; align-items: center; gap: 12px;'>
                            <div style='font-size: 13px; font-weight: 600; color: #4f46e5;'>
                                {app['ats_score']}% ATS
                            </div>
                            <div style='font-size: 12px; font-weight: 500; color: {status_color};
                                        background: {status_color}20; padding: 3px 10px;
                                        border-radius: 99px;'>
                                {app['status']}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with col_right:
        st.markdown("<div class='section-header'>How It Works</div>", unsafe_allow_html=True)

        steps = [
            ("1", "Upload Resume", "Paste or upload your current resume PDF"),
            ("2", "Add Job Description", "Paste the job posting you're applying for"),
            ("3", "Get ATS Score", "See how well your resume matches instantly"),
            ("4", "AI Rewrites It", "One click — resume tailored to that exact job"),
            ("5", "Prep Interview", "Get likely questions before you walk in"),
        ]

        for num, title, desc in steps:
            st.markdown(f"""
            <div style='display: flex; gap: 14px; margin-bottom: 16px; align-items: flex-start;'>
                <div style='min-width: 28px; height: 28px; background: #4f46e5;
                            border-radius: 50%; display: flex; align-items: center;
                            justify-content: center; font-size: 12px; font-weight: 700;
                            color: white; flex-shrink: 0; margin-top: 2px;'>
                    {num}
                </div>
                <div>
                    <div style='font-size: 13px; font-weight: 600; color: #fff;'>{title}</div>
                    <div style='font-size: 12px; color: #6b7280; margin-top: 2px;'>{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color: #2d2f3e; margin: 20px 0;'>", unsafe_allow_html=True)

        st.markdown("""
        <div class='sh-card' style='border-color: #4f46e5; background: linear-gradient(135deg, #1e1b4b, #1a1d27);'>
            <div style='font-size: 13px; font-weight: 600; color: #a5b4fc; margin-bottom: 8px;'>
                ⚡ Amazon Tip
            </div>
            <div style='font-size: 12px; color: #9ca3af; line-height: 1.6;'>
                Amazon's ATS filters resumes for Leadership Principle keywords.
                Use words like <span style='color: #a5b4fc;'>ownership, delivered, customer, 
                simplified, innovated</span> in your bullet points.
            </div>
        </div>
        """, unsafe_allow_html=True)
