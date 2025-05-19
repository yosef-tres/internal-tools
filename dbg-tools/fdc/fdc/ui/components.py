"""Basic UI components for the Fast & Dirty Commit app."""

import streamlit as st
import pandas as pd
from fdc.db.models import Collection, CollectionPart

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

    conn = st.connection('sql')
    
    if selected_table == "collection":
        with conn.session as s:
            data = s.query(Collection).all()
            if data:
                # Convert to pandas DataFrame, expand with nice columns
                data = pd.DataFrame([item.__dict__ for item in data])
                st.info("Asdfsad")
                # Remove SQLAlchemy internal state column
                if '_sa_instance_state' in data.columns:
                    data = data.drop('_sa_instance_state', axis=1)
                # Select and reorder columns
                data = data[['id', 'name', 'description', 'created_at', 'updated_at']]
            else:
                st.info("No collections found.")
    elif selected_table == "collection_part":
        collection_id = st.number_input("Collection ID", min_value=1, value=1)
        with conn.session as s:
            # Verify collection exists
            collection = s.query(Collection).filter(Collection.id == collection_id).first()
            if collection:
                st.write(f"Viewing parts for collection: {collection.name}")
                data = s.query(CollectionPart).filter(CollectionPart.collection_id == collection_id).all()
                if data:
                    # Convert SQLAlchemy objects to dict first for cleaner DataFrame conversion
                    data = pd.DataFrame([item.__dict__ for item in data])
                    # Remove SQLAlchemy internal state column
                    if '_sa_instance_state' in data.columns:
                        data = data.drop('_sa_instance_state', axis=1)
                    # Select and reorder columns
                    data = data[['id', 'collection_id', 'name', 'content', 'data', 'order', 'created_at', 'updated_at']]
                else:
                    st.info(f"No parts found for collection ID {collection_id}")
            else:
                st.error(f"Collection with ID {collection_id} not found")
    else:
        # Display not supported table message
        st.info(f"Table {selected_table} not supported.")
    # Check if we have data to display
    if isinstance(data, pd.DataFrame) and not data.empty:
        # Format datetime columns for better display
        for col in data.columns:
            if pd.api.types.is_datetime64_any_dtype(data[col]):
                data[col] = data[col].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Display as a styled table with highlighting and sorting
        st.dataframe(
            data,
            use_container_width=True,
            column_config={
                # Customize column display as needed
                'id': st.column_config.NumberColumn('ID', format='%d'),
                'created_at': st.column_config.DatetimeColumn('Created'),
                'updated_at': st.column_config.DatetimeColumn('Updated'),
                'description': st.column_config.TextColumn('Description', width='large')
            },
            hide_index=True
        )
    elif isinstance(data, pd.DataFrame):
        st.info(f"No data available for {selected_table}")
    
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
