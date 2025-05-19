"""Sidebar UI components for the Fast & Dirty Commit app."""

import streamlit as st
import pandas as pd
import plotly.express as px
import random
from fdc.data import get_db_tables
from fdc.db.session import conn

def render_sidebar():
    """Render the sidebar with database explorer and stats."""
    with st.sidebar:
        st.header("Database Explorer")
        tables = get_db_tables()
        
        # If the selected_table is not yet in session_state, initialize it
        if "selected_table" not in st.session_state:
            st.session_state.selected_table = "collections"
            
        # Create the table selector
        selected_table = st.selectbox(
            "Select Table:", 
            tables, 
            index=tables.index(st.session_state.selected_table)
        )
        st.session_state.selected_table = selected_table
        
        # Quick stats section
        st.divider()
        st.subheader("Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            with conn.session as s:
                from fdc.db.models import Collection, CollectionPart
                collection_count = s.query(Collection).count()
                st.metric("Collections", f"{collection_count:,}")
        
        with col2:
            # Show real parts count if database session is available
            with conn.session as s:
                from fdc.db.models import Collection, CollectionPart
                parts_count = s.query(CollectionPart).count()
                st.metric("Collection Parts", f"{parts_count:,}")
        
        # Simple mock visualizations
        st.divider()
        st.subheader("Transaction Activity")
        data = pd.DataFrame({
            'date': pd.date_range(start='2023-01-01', periods=10),
            'count': [random.randint(50, 300) for _ in range(10)]
        })
        fig = px.line(data, x='date', y='count')
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)
        
    # Return the selected table for easy access
    return st.session_state.selected_table
