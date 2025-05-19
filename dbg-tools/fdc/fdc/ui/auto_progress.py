"""Auto progress update functionality for the Fast & Dirty Commit app."""

import streamlit as st
import time

def update_progress():
    """Update progress for running processes (for demo purposes)."""
    # Auto-increment progress for collecting stage
    if st.session_state.collect_status == "running" and st.session_state.progress["collect"] < 1.0:
        st.session_state.progress["collect"] += 0.1
        if st.session_state.progress["collect"] >= 1.0:
            st.session_state.collect_status = "completed"
            st.session_state.progress["collect"] = 1.0
        time.sleep(0.1)
        st.rerun()
    
    # Auto-increment progress for enriching stage
    if st.session_state.enrich_status == "running" and st.session_state.progress["enrich"] < 1.0:
        st.session_state.progress["enrich"] += 0.08
        if st.session_state.progress["enrich"] >= 1.0:
            st.session_state.enrich_status = "completed"
            st.session_state.progress["enrich"] = 1.0
        time.sleep(0.1)
        st.rerun()
    
    # Auto-increment progress for building stage
    if st.session_state.build_status == "running" and st.session_state.progress["build"] < 1.0:
        st.session_state.progress["build"] += 0.05
        if st.session_state.progress["build"] >= 1.0:
            st.session_state.build_status = "completed"
            st.session_state.progress["build"] = 1.0
        time.sleep(0.1)
        st.rerun()
