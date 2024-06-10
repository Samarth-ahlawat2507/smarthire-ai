import streamlit as st
from utils.ai_engine import rewrite_resume
from utils.resume_parser import extract_text_from_pdf


def show():
    st.markdown("""
    <div style='padding: 8px 0 24px 0;'>
        <div style='font-size: 26px; font-weight: 700; color: #fff;'>✏️ AI Resume Rewriter</div>
        <div style='font-size: 14px; color: #6b7280; margin-top: 6px;'>
            AI rewrites your resume specifically for each job. Sounds human. Passes ATS. Takes 30 seconds.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Check if data carried over from ATS analyzer
    carried = False
    if 'last_resume' in st.session_state and 'last_jd' in st.session_state:
        carried = True
        st.markdown("""
        <div style='background: #1e2235; border: 1px solid #4f46e5; border-radius: 8px;
                    padding: 12px 16px; margin-bottom: 16px; font-size: 13px; color: #a5b4fc;'>
            ✓ Resume and job description loaded from your ATS analysis
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div style='font-size: 13px; font-weight: 500; color: #9ca3af; margin-bottom: 8px;'>Your Resume</div>",
                    unsafe_allow_html=True)

        default_resume = st.session_state.get('last_resume', '')

        input_method = st.radio("Method", ["Paste text", "Upload PDF"],
                                horizontal=True, label_visibility="collapsed")

        resume_text = ""
        if input_method == "Upload PDF":
            uploaded = st.file_uploader("Upload PDF", type=['pdf'],
                                        label_visibility="collapsed")
            if uploaded:
                resume_text = extract_text_from_pdf(uploaded)
        else:
            resume_text = st.text_area(
                "Resume",
                value=default_resume,
                height=300,
                label_visibility="collapsed",
                placeholder="Paste your current resume here..."
            )

    with col2:
        st.markdown("<div style='font-size: 13px; font-weight: 500; color: #9ca3af; margin-bottom: 8px;'>Job Description</div>",
                    unsafe_allow_html=True)

        default_jd = st.session_state.get('last_jd', '')

        job_desc = st.text_area(
            "Job description",
            value=default_jd,
            height=300,
            label_visibility="collapsed",
            placeholder="Paste the job description you're targeting..."
        )

        st.markdown("<div style='font-size: 13px; font-weight: 500; color: #9ca3af; margin: 8px 0;'>Tone</div>",
                    unsafe_allow_html=True)

        tone = st.select_slider(
            "Tone",
            options=["Conservative", "Professional", "Confident", "Bold"],
            value="Professional",
            label_visibility="collapsed"
        )

    st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)
    rewrite_btn = st.button("✏️ Rewrite My Resume Now", use_container_width=True)

    if rewrite_btn:
        if not resume_text or not job_desc:
            st.warning("Please add both your resume and job description.")
            return

        with st.spinner("AI is rewriting your resume... This takes about 15 seconds"):
            try:
                result = rewrite_resume(resume_text, job_desc, tone.lower())

                st.markdown("<hr style='border-color: #2d2f3e; margin: 24px 0;'>", unsafe_allow_html=True)

                # Score improvement banner
                improvement = result.get('estimated_score_improvement', 0)
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1e2235, #0d1f0d);
                            border: 1px solid #166534; border-radius: 10px;
                            padding: 16px 20px; margin-bottom: 20px;
                            display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <div style='font-size: 13px; font-weight: 600; color: #4ade80;'>
                            ✓ Resume successfully rewritten
                        </div>
                        <div style='font-size: 12px; color: #6b7280; margin-top: 4px;'>
                            Estimated ATS score improvement: +{improvement} points
                        </div>
                    </div>
                    <div style='font-size: 28px; font-weight: 700; color: #4ade80;'>
                        +{improvement}pts
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col_new, col_changes = st.columns([3, 2])

                with col_new:
                    st.markdown("<div class='section-header'>Rewritten Resume</div>",
                                unsafe_allow_html=True)

                    rewritten = result.get('rewritten_resume', '')
                    st.text_area(
                        "Copy this",
                        value=rewritten,
                        height=400,
                        label_visibility="collapsed"
                    )

                    # Download button
                    st.download_button(
                        "⬇️ Download Rewritten Resume",
                        data=rewritten,
                        file_name="resume_optimized.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                with col_changes:
                    # Key changes
                    changes = result.get('key_changes', [])
                    st.markdown("""
                    <div class='sh-card'>
                        <div style='font-size: 13px; font-weight: 600; color: #a5b4fc;
                                    margin-bottom: 12px;'>What Changed</div>
                    """, unsafe_allow_html=True)
                    for change in changes:
                        st.markdown(f"""
                        <div style='display: flex; gap: 8px; margin-bottom: 10px;
                                    align-items: flex-start;'>
                            <span style='color: #4f46e5; font-size: 12px; margin-top: 2px;'>→</span>
                            <span style='font-size: 12px; color: #d1d5db;'>{change}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                    # Keywords added
                    keywords = result.get('keywords_added', [])
                    st.markdown("""
                    <div class='sh-card'>
                        <div style='font-size: 13px; font-weight: 600; color: #4ade80;
                                    margin-bottom: 12px;'>Keywords Added</div>
                    """, unsafe_allow_html=True)
                    chips = " ".join([f'<span class="badge-blue">{kw}</span>'
                                      for kw in keywords])
                    st.markdown(f"{chips}</div>", unsafe_allow_html=True)

                    # Pro tips
                    tips = result.get('tips', [])
                    st.markdown("""
                    <div class='sh-card-highlight'>
                        <div style='font-size: 13px; font-weight: 600; color: #a5b4fc;
                                    margin-bottom: 12px;'>💡 Pro Tips</div>
                    """, unsafe_allow_html=True)
                    for tip in tips:
                        st.markdown(f"""
                        <div style='font-size: 12px; color: #9ca3af; margin-bottom: 8px;
                                    padding-left: 12px; border-left: 2px solid #4f46e5;'>
                            {tip}
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Rewrite failed: {str(e)}")
