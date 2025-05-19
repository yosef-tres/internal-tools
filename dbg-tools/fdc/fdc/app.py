"""Streamlit app for Fast & Dirty Commit - Blockchain Transaction Processing."""

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
from fdc.db.session import conn
from fdc.db.models import Collection


def app():
    """Main Streamlit app."""
    # App configuration
    st.set_page_config(
        page_title="Fast & Dirty Commit - Blockchain Processor",
        page_icon="",
        layout="wide",
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Title and description
    st.title(" - Blockchain Transaction Processor")
    st.markdown("Internal tool for collecting, enriching, and building blockchain transaction data")
    
    # Render sidebar and get selected table
    render_sidebar()
    
    # For demonstration purposes, create a sample collection if none exist
    with conn.session as s:
        collections = s.query(Collection).all()
        if not collections:
            st.info("Creating a sample collection...")
            from fdc.data import create_sample_collection
            sample = create_sample_collection(db, name="Sample Collection", description="A demonstration collection")
            st.success(f"Created sample collection: {sample.name} with {len(sample.parts)} parts")
    
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
        if st.session_state.selected_table == "collections":
            st.subheader("Collections")
            with conn.session as s:
                from fdc.data import get_collections_data
                collections_data = get_collections_data(s)
                if collections_data:
                    st.dataframe(collections_data)
                else:
                    st.info("No collections found.")
        elif st.session_state.selected_table == "collection_parts":
            st.subheader("Collection Parts")
            collection_id = st.number_input("Collection ID", min_value=1, value=1)
            with conn.session as s:
                # Verify collection exists
                collection = s.query(Collection).filter(Collection.id == collection_id).first()
                if collection:
                    st.write(f"Viewing parts for collection: {collection.name}")
                    from fdc.data import get_collection_parts_data
                    parts_data = get_collection_parts_data(s, collection_id)
                    if parts_data:
                        st.dataframe(parts_data)
                    else:
                        st.info(f"No parts found for collection ID {collection_id}")
                else:
                    st.error(f"Collection with ID {collection_id} not found")
        else:
            # For backward compatibility with any other tables
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
        st.session_state.selected_table = "collections"
    if "db_session" not in st.session_state:
        st.session_state.db_session = None


if __name__ == "__main__":
    app()
