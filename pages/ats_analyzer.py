import streamlit as st
from utils.ai_engine import analyze_ats_score
from utils.resume_parser import extract_text_from_pdf, get_score_color, get_score_label
from utils.database import log_analysis


def show():
    st.markdown("""
    <div style='padding: 8px 0 24px 0;'>
        <div style='font-size: 26px; font-weight: 700; color: #fff;'>📄 ATS Score Analyzer</div>
        <div style='font-size: 14px; color: #6b7280; margin-top: 6px;'>
            See exactly how your resume scores against any job description. Fix what's missing before you apply.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div style='font-size: 13px; font-weight: 500; color: #9ca3af; margin-bottom: 8px;'>Your Resume</div>",
                    unsafe_allow_html=True)

        input_method = st.radio("Input method", ["Paste text", "Upload PDF"],
                                horizontal=True, label_visibility="collapsed")

        resume_text = ""
        if input_method == "Upload PDF":
            uploaded = st.file_uploader("Upload resume PDF", type=['pdf'],
                                        label_visibility="collapsed")
            if uploaded:
                resume_text = extract_text_from_pdf(uploaded)
                if resume_text and not resume_text.startswith("Error"):
                    st.success(f"Resume loaded — {len(resume_text.split())} words extracted")
                else:
                    st.error(resume_text)
        else:
            resume_text = st.text_area(
                "Paste resume",
                height=280,
                placeholder="Paste your full resume text here...",
                label_visibility="collapsed"
            )

    with col2:
        st.markdown("<div style='font-size: 13px; font-weight: 500; color: #9ca3af; margin-bottom: 8px;'>Job Description</div>",
                    unsafe_allow_html=True)

        company_name = st.text_input("Company name (optional)",
                                     placeholder="e.g. Amazon, Flipkart, Adobe...",
                                     label_visibility="collapsed")

        job_desc = st.text_area(
            "Job description",
            height=280,
            placeholder="Paste the full job description here...",
            label_visibility="collapsed"
        )

    st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)

    analyze_btn = st.button("⚡ Analyze ATS Score", use_container_width=True)

    if analyze_btn:
        if not resume_text or not job_desc:
            st.warning("Please add both your resume and the job description.")
            return

        with st.spinner("Analyzing your resume against the job description..."):
            try:
                result = analyze_ats_score(resume_text, job_desc)

                # Log to database
                log_analysis(
                    company=company_name or "Unknown",
                    role="SDE",
                    ats_score=result.get('overall_score', 0),
                    keywords_matched=len(result.get('matched_keywords', [])),
                    keywords_missing=len(result.get('missing_keywords', []))
                )

                # Store in session for rewriter
                st.session_state['last_analysis'] = result
                st.session_state['last_resume'] = resume_text
                st.session_state['last_jd'] = job_desc

                show_results(result)

            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                st.info("Make sure your ANTHROPIC_API_KEY is set in environment variables.")


def show_results(result: dict):
    score = result.get('overall_score', 0)
    color = get_score_color(score)
    label = get_score_label(score)

    st.markdown("<hr style='border-color: #2d2f3e; margin: 24px 0;'>", unsafe_allow_html=True)

    # Main score + sub scores
    col_score, col_breakdown = st.columns([1, 2])

    with col_score:
        st.markdown(f"""
        <div class='sh-card' style='text-align: center; padding: 32px 24px;
                    border-color: {color}40;'>
            <div style='font-size: 72px; font-weight: 700; color: {color};
                        line-height: 1;'>{score}</div>
            <div style='font-size: 16px; font-weight: 600; color: {color};
                        margin-top: 4px;'>{label}</div>
            <div style='font-size: 13px; color: #6b7280; margin-top: 8px;'>ATS Match Score</div>
            <hr style='border-color: #2d2f3e; margin: 16px 0;'>
            <div style='font-size: 12px; color: #9ca3af; font-style: italic;'>
                "{result.get('verdict', '')}"
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_breakdown:
        st.markdown("<div class='section-header'>Score Breakdown</div>", unsafe_allow_html=True)

        sub_scores = [
            ("Keywords Match", result.get('keyword_score', 0)),
            ("Skills Alignment", result.get('skills_score', 0)),
            ("Experience Match", result.get('experience_score', 0)),
            ("Format & Structure", result.get('format_score', 0)),
        ]

        for label_text, sub_score in sub_scores:
            sub_color = get_score_color(sub_score)
            st.markdown(f"""
            <div style='margin-bottom: 14px;'>
                <div style='display: flex; justify-content: space-between;
                            font-size: 13px; margin-bottom: 6px;'>
                    <span style='color: #d1d5db;'>{label_text}</span>
                    <span style='font-weight: 600; color: {sub_color};'>{sub_score}%</span>
                </div>
                <div class='progress-wrap'>
                    <div class='progress-fill' style='width: {sub_score}%;
                                background: {sub_color};'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 8px 0;'></div>", unsafe_allow_html=True)

    # Keywords section
    col_matched, col_missing = st.columns(2)

    with col_matched:
        matched = result.get('matched_keywords', [])
        st.markdown(f"""
        <div class='sh-card' style='border-color: #16653440;'>
            <div style='font-size: 13px; font-weight: 600; color: #4ade80; margin-bottom: 12px;'>
                ✓ Matched Keywords ({len(matched)})
            </div>
        """, unsafe_allow_html=True)
        chips = " ".join([f'<span class="badge-green">{kw}</span>' for kw in matched])
        st.markdown(f"{chips}</div>", unsafe_allow_html=True)

    with col_missing:
        missing = result.get('missing_keywords', [])
        st.markdown(f"""
        <div class='sh-card' style='border-color: #7f1d1d40;'>
            <div style='font-size: 13px; font-weight: 600; color: #f87171; margin-bottom: 12px;'>
                ✗ Missing Keywords ({len(missing)})
            </div>
        """, unsafe_allow_html=True)
        chips = " ".join([f'<span class="badge-red">{kw}</span>' for kw in missing])
        st.markdown(f"{chips}</div>", unsafe_allow_html=True)

    # Strengths and weaknesses
    col_str, col_weak = st.columns(2)

    with col_str:
        strengths = result.get('strengths', [])
        st.markdown("""
        <div class='sh-card'>
            <div style='font-size: 13px; font-weight: 600; color: #4ade80; margin-bottom: 12px;'>
                💪 Strengths
            </div>
        """, unsafe_allow_html=True)
        for s in strengths:
            st.markdown(f"""
            <div style='display: flex; gap: 8px; margin-bottom: 8px; align-items: flex-start;'>
                <span style='color: #4ade80; font-size: 12px; margin-top: 1px;'>✓</span>
                <span style='font-size: 13px; color: #d1d5db;'>{s}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_weak:
        weaknesses = result.get('weaknesses', [])
        st.markdown("""
        <div class='sh-card'>
            <div style='font-size: 13px; font-weight: 600; color: #f87171; margin-bottom: 12px;'>
                ⚠️ Weaknesses
            </div>
        """, unsafe_allow_html=True)
        for w in weaknesses:
            st.markdown(f"""
            <div style='display: flex; gap: 8px; margin-bottom: 8px; align-items: flex-start;'>
                <span style='color: #f87171; font-size: 12px; margin-top: 1px;'>✗</span>
                <span style='font-size: 13px; color: #d1d5db;'>{w}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Quick fixes
    fixes = result.get('quick_fixes', [])
    if fixes:
        st.markdown("""
        <div class='sh-card-highlight'>
            <div style='font-size: 13px; font-weight: 600; color: #a5b4fc; margin-bottom: 12px;'>
                ⚡ Quick Fixes to Boost Your Score
            </div>
        """, unsafe_allow_html=True)
        for i, fix in enumerate(fixes, 1):
            st.markdown(f"""
            <div style='display: flex; gap: 12px; margin-bottom: 10px; align-items: flex-start;'>
                <div style='min-width: 22px; height: 22px; background: #4f46e5;
                            border-radius: 50%; display: flex; align-items: center;
                            justify-content: center; font-size: 11px; font-weight: 700;
                            color: white; flex-shrink: 0;'>{i}</div>
                <div style='font-size: 13px; color: #d1d5db; padding-top: 2px;'>{fix}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # CTA
    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
    if st.button("✏️ Auto-Rewrite Resume for This Job →", use_container_width=True):
        st.info("Go to '✏️ Resume Rewriter' in the sidebar — your resume and JD are already loaded!")
