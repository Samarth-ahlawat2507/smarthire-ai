import streamlit as st
from utils.ai_engine import generate_interview_questions
from utils.resume_parser import extract_text_from_pdf


def show():
    st.markdown("""
    <div style='padding: 8px 0 24px 0;'>
        <div style='font-size: 26px; font-weight: 700; color: #fff;'>🎯 Interview Prep</div>
        <div style='font-size: 14px; color: #6b7280; margin-top: 6px;'>
            Know exactly what questions to expect before you walk in. Based on your resume + the actual job.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("<div style='font-size: 13px; font-weight: 500; color: #9ca3af; margin-bottom: 8px;'>Your Resume</div>",
                    unsafe_allow_html=True)

        default_resume = st.session_state.get('last_resume', '')
        resume_text = st.text_area(
            "Resume",
            value=default_resume,
            height=220,
            label_visibility="collapsed",
            placeholder="Paste your resume here..."
        )

    with col2:
        st.markdown("<div style='font-size: 13px; font-weight: 500; color: #9ca3af; margin-bottom: 8px;'>Job Description</div>",
                    unsafe_allow_html=True)

        default_jd = st.session_state.get('last_jd', '')
        job_desc = st.text_area(
            "JD",
            value=default_jd,
            height=160,
            label_visibility="collapsed",
            placeholder="Paste the job description..."
        )

        company = st.selectbox(
            "Target company",
            ["Amazon", "Microsoft", "Google", "Flipkart", "Adobe",
             "Razorpay", "PhonePe", "Swiggy", "Atlassian", "Other"],
            label_visibility="collapsed"
        )

    st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)
    prep_btn = st.button("🎯 Generate Interview Questions", use_container_width=True)

    if prep_btn:
        if not resume_text or not job_desc:
            st.warning("Please add both resume and job description.")
            return

        with st.spinner(f"Generating likely {company} interview questions based on your profile..."):
            try:
                result = generate_interview_questions(resume_text, job_desc, company)

                st.markdown("<hr style='border-color: #2d2f3e; margin: 24px 0;'>",
                            unsafe_allow_html=True)

                tab1, tab2, tab3, tab4 = st.tabs([
                    "💻 Technical", "🧠 Leadership (LP)", "📁 Project", "📚 DSA Topics"
                ])

                with tab1:
                    tech_qs = result.get('technical_questions', [])
                    st.markdown(f"""
                    <div style='font-size: 12px; color: #6b7280; margin-bottom: 16px;'>
                        {len(tech_qs)} technical questions predicted for your profile
                    </div>
                    """, unsafe_allow_html=True)

                    for i, q in enumerate(tech_qs, 1):
                        with st.expander(f"Q{i}: {q.get('question', '')}"):
                            st.markdown(f"""
                            <div style='margin-bottom: 10px;'>
                                <span style='font-size: 11px; color: #6b7280;
                                            text-transform: uppercase; letter-spacing: 0.05em;'>
                                    Why they ask this
                                </span>
                                <div style='font-size: 13px; color: #d1d5db; margin-top: 4px;'>
                                    {q.get('why_asked', '')}
                                </div>
                            </div>
                            <div style='background: #1e2235; border: 1px solid #4f46e5;
                                        border-radius: 8px; padding: 12px; margin-top: 8px;'>
                                <div style='font-size: 11px; color: #a5b4fc; margin-bottom: 4px;
                                            font-weight: 600;'>💡 HINT</div>
                                <div style='font-size: 13px; color: #9ca3af;'>{q.get('hint', '')}</div>
                            </div>
                            """, unsafe_allow_html=True)

                with tab2:
                    lp_qs = result.get('behavioral_questions', [])
                    st.markdown(f"""
                    <div style='background: #1a1d27; border: 1px solid #2d2f3e;
                                border-radius: 8px; padding: 12px 16px; margin-bottom: 16px;'>
                        <div style='font-size: 12px; color: #a5b4fc; font-weight: 600;'>
                            ⚡ Amazon LP Round Info
                        </div>
                        <div style='font-size: 12px; color: #6b7280; margin-top: 4px;'>
                            Every round at Amazon has LP questions. Answer using STAR format:
                            Situation → Task → Action → Result (with numbers).
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    for i, q in enumerate(lp_qs, 1):
                        with st.expander(f"LP Q{i}: {q.get('question', '')}"):
                            st.markdown(f"""
                            <div style='margin-bottom: 10px;'>
                                <span class='badge-blue'>{q.get('lp', '')}</span>
                            </div>
                            <div style='background: #1e2235; border: 1px solid #4f46e5;
                                        border-radius: 8px; padding: 12px; margin-top: 8px;'>
                                <div style='font-size: 11px; color: #a5b4fc; margin-bottom: 4px;
                                            font-weight: 600;'>STAR HINT</div>
                                <div style='font-size: 13px; color: #9ca3af;'>
                                    {q.get('star_hint', '')}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                with tab3:
                    proj_qs = result.get('project_questions', [])
                    st.markdown("""
                    <div style='font-size: 12px; color: #6b7280; margin-bottom: 16px;'>
                        These are questions about YOUR specific projects from your resume.
                        You must know every answer cold.
                    </div>
                    """, unsafe_allow_html=True)

                    for i, q in enumerate(proj_qs, 1):
                        with st.expander(f"Project Q{i}: {q.get('question', '')}"):
                            st.markdown(f"""
                            <div style='background: #1e2235; border: 1px solid #4f46e5;
                                        border-radius: 8px; padding: 12px;'>
                                <div style='font-size: 11px; color: #a5b4fc; margin-bottom: 4px;
                                            font-weight: 600;'>WHAT THEY WANT TO HEAR</div>
                                <div style='font-size: 13px; color: #9ca3af;'>
                                    {q.get('what_they_want', '')}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                with tab4:
                    dsa_topics = result.get('dsa_topics', [])
                    tips = result.get('preparation_tips', [])

                    st.markdown("<div class='section-header'>Likely DSA Topics for This Role</div>",
                                unsafe_allow_html=True)

                    cols = st.columns(2)
                    for i, topic in enumerate(dsa_topics):
                        with cols[i % 2]:
                            st.markdown(f"""
                            <div class='sh-card' style='padding: 12px 16px; margin-bottom: 8px;'>
                                <span style='font-size: 13px; color: #d1d5db;'>📌 {topic}</span>
                            </div>
                            """, unsafe_allow_html=True)

                    st.markdown("<div class='section-header' style='margin-top: 20px;'>Prep Tips</div>",
                                unsafe_allow_html=True)

                    for tip in tips:
                        st.markdown(f"""
                        <div style='display: flex; gap: 10px; margin-bottom: 10px;
                                    align-items: flex-start;'>
                            <span style='color: #4f46e5; font-size: 14px;'>→</span>
                            <span style='font-size: 13px; color: #d1d5db;'>{tip}</span>
                        </div>
                        """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Generation failed: {str(e)}")
