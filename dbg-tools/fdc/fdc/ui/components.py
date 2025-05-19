"""Basic UI components for the Fast & Dirty Commit app."""

import streamlit as st
import pandas as pd
from datetime import datetime
import random
from fdc.data import get_mock_transactions, get_mock_entities

def render_status_indicator(status, stage_name):
    """Render a status indicator for a process stage."""
    if status == "idle":
        st.info(f"{stage_name}: Idle")
    elif status == "running":
        st.success(f"{stage_name}: Running")
    elif status == "completed":
        st.success(f"{stage_name}: Completed")
    elif status == "error":
        st.error(f"{stage_name}: Error")
    else:
        st.warning(f"{stage_name}: {status}")

def render_process_controls(stage_name, status):
    """Render control buttons for a process stage."""
    col1, col2, col3 = st.columns(3)
    with col1:
        if status != "running":
            start_btn = st.button(f"Start {stage_name}", key=f"start_{stage_name.lower()}")
        else:
            start_btn = st.button(f"Start {stage_name}", key=f"start_{stage_name.lower()}", disabled=True)
    
    with col2:
        if status == "running":
            stop_btn = st.button(f"Stop {stage_name}", key=f"stop_{stage_name.lower()}")
        else:
            stop_btn = st.button(f"Stop {stage_name}", key=f"stop_{stage_name.lower()}", disabled=True)
    
    with col3:
        reset_btn = st.button(f"Reset {stage_name}", key=f"reset_{stage_name.lower()}")
    
    return {"start": start_btn, "stop": stop_btn, "reset": reset_btn}

def render_db_viewer(selected_table):
    """Render the database viewer component."""
    st.subheader(f"Database Table: {selected_table}")
    
    # Mock data based on selected table
    if selected_table == "transactions":
        data = pd.DataFrame(get_mock_transactions(20))
    elif selected_table == "entities":
        data = pd.DataFrame(get_mock_entities(15))
    elif selected_table == "addresses":
        data = pd.DataFrame(get_mock_entities(10))
    else:
        # Generic mock data for other tables
        data = pd.DataFrame({
            "id": [f"ID-{i}" for i in range(10)],
            "created_at": [datetime.now().strftime("%Y-%m-%d %H:%M:%S") for _ in range(10)],
            "field1": [f"Value {random.randint(1, 100)}" for _ in range(10)],
            "field2": [random.choice(["Active", "Inactive", "Pending"]) for _ in range(10)],
        })
    
    # Table filters (basic functionality)
    with st.expander("Table Filters"):
        col1, col2 = st.columns(2)
        
        # This is just a UI placeholder for actual filters
        with col1:
            st.text_input("Search:", placeholder="Search in table...")
            st.selectbox("Status:", ["All", "Active", "Inactive", "Pending"])
        
        with col2:
            st.date_input("From Date:")
            st.date_input("To Date:")
    
    # Show table data with pagination controls
    st.dataframe(data, use_container_width=True)
    
    # Pagination UI (placeholder for actual pagination)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.button("← Previous")
    with col2:
        st.write("Page 1 of 1")
    with col3:
        st.button("Next →")
    
    # Export buttons
    st.download_button(
        "Export as CSV",
        data.to_csv(index=False).encode('utf-8'),
        f"{selected_table}.csv",
        "text/csv",
        key=f"export_{selected_table}"
    )
