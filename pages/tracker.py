import streamlit as st
from utils.database import (get_all_applications, add_application,
                             update_application_status, delete_application, get_stats)


STATUS_OPTIONS = ["Applied", "OA Sent", "OA Done", "Interviewing",
                  "Offer Received", "Rejected", "Withdrawn"]

STATUS_COLORS = {
    "Applied": "#fbbf24",
    "OA Sent": "#60a5fa",
    "OA Done": "#a78bfa",
    "Interviewing": "#34d399",
    "Offer Received": "#4ade80",
    "Rejected": "#f87171",
    "Withdrawn": "#6b7280"
}


def show():
    st.markdown("""
    <div style='padding: 8px 0 24px 0;'>
        <div style='font-size: 26px; font-weight: 700; color: #fff;'>📊 Application Tracker</div>
        <div style='font-size: 14px; color: #6b7280; margin-top: 6px;'>
            Track every application in one place. Know exactly where you stand with each company.
        </div>
    </div>
    """, unsafe_allow_html=True)

    stats = get_stats()
    apps = get_all_applications()

    # Stats row
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    metrics = [
        (c1, "Total", stats['total'], None),
        (c2, "Applied", stats['applied'], "#fbbf24"),
        (c3, "Interviewing", stats['interviewing'], "#34d399"),
        (c4, "Offers", stats['offered'], "#4ade80"),
        (c5, "Rejected", stats['rejected'], "#f87171"),
        (c6, "Avg ATS", f"{stats['avg_ats']}%", "#a5b4fc"),
    ]

    for col, label, value, color in metrics:
        with col:
            color_str = f"color: {color};" if color else ""
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value' style='{color_str}'>{value}</div>
                <div class='metric-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)

    col_form, col_list = st.columns([1, 2])

    with col_form:
        st.markdown("<div class='section-header'>Log New Application</div>",
                    unsafe_allow_html=True)

        with st.container():
            company = st.text_input("Company", placeholder="e.g. Amazon")
            role = st.text_input("Role", placeholder="e.g. SDE1 - Backend")
            ats_score = st.slider("ATS Score", 0, 100, 65)

            col_a, col_b = st.columns(2)
            with col_a:
                salary = st.text_input("Salary range", placeholder="e.g. 20-32 LPA")
            with col_b:
                job_url = st.text_input("Job URL", placeholder="paste link...")

            notes = st.text_area("Notes", placeholder="Any notes about this application...",
                                 height=80)

            if st.button("➕ Add Application", use_container_width=True):
                if company and role:
                    add_application(
                        company=company,
                        role=role,
                        ats_score=ats_score,
                        job_url=job_url,
                        salary_range=salary,
                        notes=notes
                    )
                    st.success(f"✓ Added {role} at {company}")
                    st.rerun()
                else:
                    st.warning("Please add company name and role.")

    with col_list:
        st.markdown("<div class='section-header'>All Applications</div>",
                    unsafe_allow_html=True)

        if not apps:
            st.markdown("""
            <div class='sh-card' style='text-align: center; padding: 40px;'>
                <div style='font-size: 32px; margin-bottom: 12px;'>📭</div>
                <div style='font-size: 14px; color: #6b7280;'>
                    No applications yet.<br>Add your first one on the left.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Filter
            status_filter = st.multiselect(
                "Filter by status",
                STATUS_OPTIONS,
                default=[],
                placeholder="All statuses",
                label_visibility="collapsed"
            )

            filtered = apps if not status_filter else [
                a for a in apps if a['status'] in status_filter
            ]

            for app in filtered:
                status = app['status']
                color = STATUS_COLORS.get(status, '#6b7280')
                score = app['ats_score']
                score_color = "#4ade80" if score >= 70 else "#fbbf24" if score >= 50 else "#f87171"

                with st.expander(
                    f"{app['company']} — {app['role']} | ATS: {score}%"
                ):
                    col_details, col_actions = st.columns([2, 1])

                    with col_details:
                        st.markdown(f"""
                        <div style='margin-bottom: 8px;'>
                            <span style='color: {color}; background: {color}20;
                                         padding: 3px 10px; border-radius: 99px;
                                         font-size: 12px; font-weight: 500;'>
                                {status}
                            </span>
                        </div>
                        <div style='font-size: 12px; color: #6b7280; margin-bottom: 4px;'>
                            Applied: {app['applied_date']}
                        </div>
                        """, unsafe_allow_html=True)

                        if app['salary_range']:
                            st.markdown(f"""
                            <div style='font-size: 12px; color: #4ade80;'>
                                💰 {app['salary_range']}
                            </div>
                            """, unsafe_allow_html=True)

                        if app['notes']:
                            st.markdown(f"""
                            <div style='font-size: 12px; color: #9ca3af; margin-top: 8px;
                                        padding: 8px; background: #1a1d27;
                                        border-radius: 6px; border: 1px solid #2d2f3e;'>
                                {app['notes']}
                            </div>
                            """, unsafe_allow_html=True)

                        if app['job_url']:
                            st.markdown(f"""
                            <a href='{app['job_url']}' target='_blank'
                               style='font-size: 12px; color: #4f46e5; margin-top: 6px;
                                      display: inline-block;'>
                                🔗 View Job Posting
                            </a>
                            """, unsafe_allow_html=True)

                    with col_actions:
                        new_status = st.selectbox(
                            "Update status",
                            STATUS_OPTIONS,
                            index=STATUS_OPTIONS.index(status),
                            key=f"status_{app['id']}",
                            label_visibility="collapsed"
                        )

                        if new_status != status:
                            update_application_status(app['id'], new_status)
                            st.rerun()

                        if st.button("🗑️ Delete", key=f"del_{app['id']}",
                                     use_container_width=True):
                            delete_application(app['id'])
                            st.rerun()
