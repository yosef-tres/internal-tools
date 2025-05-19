"""Streamlit app for Fast & Dirty Commit - Blockchain Transaction Processing."""

import json
import streamlit as st

# Import UI components from our modular structure - only importing what we use directly in this file
from fdc.ui import (
    render_db_viewer,
    render_sidebar,
    render_collector_stage,
    render_enricher_stage,
    render_builder_stage,
    update_progress
)

# Import database functionality
from fdc.db.models import Collection, CollectionPart


def app():
    """Main Streamlit app."""
    # App configuration
    st.set_page_config(
        page_title="Fast & Dirty Commit - Blockchain Processor",
        page_icon="",
        layout="wide",
    )

    conn = st.connection('sql')
    
    # Initialize session state
    initialize_session_state()
    
    # Title and description
    st.title(" - Blockchain Transaction Processor")
    st.markdown("Internal tool for collecting, enriching, and building blockchain transaction data")
    
    # Render sidebar and get selected table
    render_sidebar()
    
    # For demonstration purposes, create a sample collection if none exist
    with conn.session as s:
        # Create a Collection with 5 Collection Parts and commit to DB, if There are not already collections
        if not s.query(Collection).count():
            collection = Collection(name="Sample Collection", description="A demonstration collection")
            s.add(collection)
            s.commit()
            
            # Create 5 Collection Parts and commit to DB
            for i in range(5):
                collection_part = CollectionPart(
                    collection_id=collection.id,
                    name=f"Part {i+1}",
                    content=f"Sample content for the part {i+1}",
                    data=json.dumps({"type": "sample", "version": "1.0"}),
                    order=i
                )
                s.add(collection_part)
            s.commit()
        
    
    # Main content - Three-legged process
    col1, col2 = st.columns([2, 3])
    
    # Left column - Process controls
    with col1:
        st.subheader("Process Controls")
        
        # Render the three main processing stages
        render_collector_stage()
        render_enricher_stage()
        render_builder_stage()
    
    # Right column - DB Viewer
    with col2:
        # Display different views based on the selected table
        render_db_viewer(st.session_state.selected_table)
    
    # Auto-increment progress for running processes
    update_progress()


def initialize_session_state():
    """Initialize the session state variables if they don't exist."""
    if "collect_status" not in st.session_state:
        st.session_state.collect_status = "idle"
    if "enrich_status" not in st.session_state:
        st.session_state.enrich_status = "idle"
    if "build_status" not in st.session_state:
        st.session_state.build_status = "idle"
    if "progress" not in st.session_state:
        st.session_state.progress = {"collect": 0, "enrich": 0, "build": 0}
    if "selected_table" not in st.session_state:
        st.session_state.selected_table = "collection"
    if "db_session" not in st.session_state:
        st.session_state.db_session = None


if __name__ == "__main__":
    app()
