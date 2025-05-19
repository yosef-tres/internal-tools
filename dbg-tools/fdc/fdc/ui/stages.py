"""Process stage UI components for the Fast & Dirty Commit app."""

import streamlit as st
from fdc.ui.components import render_status_indicator, render_process_controls

def render_collector_stage():
    """Render the Collector stage UI components."""
    with st.expander("1. Collector", expanded=True):
        render_status_indicator(st.session_state.collect_status, "Collector")
        
        # Source selection
        sources = ["Ethereum", "Polygon", "Arbitrum", "All Chains"]
        # Store selections in session state for potential future use
        selected_sources = st.multiselect("Data Sources:", sources, default=["Ethereum"])
        if "selected_sources" not in st.session_state:
            st.session_state.selected_sources = selected_sources
        
        time_range = st.select_slider(
            "Time Range:",
            options=["Last hour", "Last 24 hours", "Last week", "Last month", "Custom"]
        )
        
        if time_range == "Custom":
            col1, col2 = st.columns(2)
            with col1:
                # Store in session state for future implementation
                start_date = st.date_input("Start Date")
                if "collection_start_date" not in st.session_state:
                    st.session_state.collection_start_date = start_date
            with col2:
                # Store in session state for future implementation
                end_date = st.date_input("End Date")
                if "collection_end_date" not in st.session_state:
                    st.session_state.collection_end_date = end_date
        
        # Controls
        controls = render_process_controls("Collector", st.session_state.collect_status)
        
        # Progress bar
        if st.session_state.collect_status == "running":
            st.progress(st.session_state.progress["collect"], text=f"Collecting: {st.session_state.progress['collect']*100:.0f}%")
        
        # Handle button clicks
        if controls["start"]:
            st.session_state.collect_status = "running"
            st.session_state.progress["collect"] = 0.1
            st.rerun()
        
        if controls["stop"] and st.session_state.collect_status == "running":
            st.session_state.collect_status = "idle"
            st.rerun()
        
        if controls["reset"]:
            st.session_state.collect_status = "idle"
            st.session_state.progress["collect"] = 0
            st.rerun()

def render_enricher_stage():
    """Render the Enricher stage UI components."""
    with st.expander("2. Enricher", expanded=True):
        render_status_indicator(st.session_state.enrich_status, "Enricher")
        
        # Enrichment options
        enrichment_options = [
            "Address Labeling", 
            "Contract Resolution", 
            "Token Data", 
            "Protocol Identification"
        ]
        # Store selections in session state for potential future use
        selected_enrichments = st.multiselect(
            "Enrichment Options:", 
            enrichment_options,
            default=enrichment_options[:2]
        )
        if "selected_enrichments" not in st.session_state:
            st.session_state.selected_enrichments = selected_enrichments
        
        # Controls
        controls = render_process_controls("Enricher", st.session_state.enrich_status)
        
        # Dependency warning
        if st.session_state.collect_status not in ["completed", "running"] and controls["start"]:
            st.warning("Collector hasn't completed yet. Enrichment may have incomplete data.")
        
        # Progress bar
        if st.session_state.enrich_status == "running":
            st.progress(st.session_state.progress["enrich"], text=f"Enriching: {st.session_state.progress['enrich']*100:.0f}%")
        
        # Handle button clicks
        if controls["start"]:
            st.session_state.enrich_status = "running"
            st.session_state.progress["enrich"] = 0.1
            st.rerun()
        
        if controls["stop"] and st.session_state.enrich_status == "running":
            st.session_state.enrich_status = "idle"
            st.rerun()
        
        if controls["reset"]:
            st.session_state.enrich_status = "idle"
            st.session_state.progress["enrich"] = 0
            st.rerun()

def render_builder_stage():
    """Render the Builder stage UI components."""
    with st.expander("3. Transaction Builder", expanded=True):
        render_status_indicator(st.session_state.build_status, "Transaction Builder")
        
        # Builder options
        builder_options = {
            "Group related transactions": True,
            "Include failed transactions": False,
            "Generate transaction summaries": True,
            "Rebuild existing transactions": False
        }
        
        for option, default in builder_options.items():
            builder_options[option] = st.checkbox(option, value=default, key=f"build_option_{option}")
        
        # Controls
        controls = render_process_controls("Builder", st.session_state.build_status)
        
        # Dependency warning
        if st.session_state.enrich_status not in ["completed", "running"] and controls["start"]:
            st.warning("Enrichment hasn't completed yet. Building may have incomplete data.")
        
        # Progress bar
        if st.session_state.build_status == "running":
            st.progress(st.session_state.progress["build"], text=f"Building: {st.session_state.progress['build']*100:.0f}%")
        
        # Handle button clicks
        if controls["start"]:
            st.session_state.build_status = "running"
            st.session_state.progress["build"] = 0.1
            st.rerun()
        
        if controls["stop"] and st.session_state.build_status == "running":
            st.session_state.build_status = "idle"
            st.rerun()
        
        if controls["reset"]:
            st.session_state.build_status = "idle"
            st.session_state.progress["build"] = 0
            st.rerun()
