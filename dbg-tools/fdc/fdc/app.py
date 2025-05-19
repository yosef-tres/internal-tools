"""Streamlit app for Fast & Dirty Commit - Blockchain Transaction Processing."""

import streamlit as st
import pandas as pd
import time
from datetime import datetime
import plotly.express as px
import random

# Mock data functions (to be replaced with actual business logic later)
def get_mock_transactions(count=10):
    """Generate mock transaction data for demonstration."""
    mock_txns = []
    blockchains = ["Ethereum", "Polygon", "Arbitrum", "Optimism", "BSC"]
    status = ["Pending", "Completed", "Failed"]
    
    for i in range(count):
        mock_txns.append({
            "id": f"0x{random.randint(10**30, 10**31):x}",
            "blockchain": random.choice(blockchains),
            "from_address": f"0x{random.randint(10**30, 10**31):x}",
            "to_address": f"0x{random.randint(10**30, 10**31):x}",
            "value": round(random.uniform(0.001, 10.0), 6),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": random.choice(status),
            "gas_used": random.randint(21000, 250000)
        })
    return mock_txns

def get_mock_entities(count=5):
    """Generate mock entity data for demonstration."""
    entity_types = ["Address", "Contract", "Token", "NFT", "Project"]
    tags = ["DEX", "CEX", "Bridge", "Wallet", "Smart Contract", "DeFi", "Gaming"]
    
    entities = []
    for i in range(count):
        entity_type = random.choice(entity_types)
        entities.append({
            "id": f"0x{random.randint(10**30, 10**31):x}",
            "type": entity_type,
            "name": f"{entity_type}-{random.randint(1000, 9999)}",
            "tags": random.sample(tags, random.randint(1, 3)),
            "first_seen": datetime.now().strftime("%Y-%m-%d"),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
    return entities

def get_mock_db_tables():
    """Return mock DB tables for the sidebar."""
    return [
        "transactions", 
        "entities", 
        "addresses", 
        "contracts", 
        "tokens", 
        "events", 
        "blocks"
    ]

# UI Components
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
            "updated_at": [datetime.now().strftime("%Y-%m-%d %H:%M:%S") for _ in range(10)],
            "field1": [f"Value-{i}" for i in range(10)],
            "field2": [random.randint(1, 1000) for _ in range(10)]
        })
    
    # Filter controls
    with st.expander("Filters", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            if "id" in data.columns:
                id_filter = st.text_input("Filter by ID:", key=f"filter_id_{selected_table}")
        with col2:
            if "status" in data.columns:
                status_filter = st.selectbox("Status:", ["All", "Pending", "Completed", "Failed"], key=f"filter_status_{selected_table}")
    
    # Display data table
    st.dataframe(data, use_container_width=True)
    
    # Export options
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "Export CSV",
            data.to_csv(index=False).encode('utf-8'),
            f"{selected_table}.csv",
            "text/csv",
            key=f"export_csv_{selected_table}"
        )
    with col2:
        st.download_button(
            "Export JSON",
            data.to_json(orient="records"),
            f"{selected_table}.json",
            "application/json",
            key=f"export_json_{selected_table}"
        )

def app():
    """Main Streamlit app."""
    # App configuration
    st.set_page_config(
        page_title="Fast & Dirty Commit - Blockchain Processor",
        page_icon="",
        layout="wide",
    )
    
    # Initialize session state
    if "collect_status" not in st.session_state:
        st.session_state.collect_status = "idle"
    if "enrich_status" not in st.session_state:
        st.session_state.enrich_status = "idle"
    if "build_status" not in st.session_state:
        st.session_state.build_status = "idle"
    if "progress" not in st.session_state:
        st.session_state.progress = {"collect": 0, "enrich": 0, "build": 0}
    if "selected_table" not in st.session_state:
        st.session_state.selected_table = "transactions"
    
    # Title and description
    st.title(" - Blockchain Transaction Processor")
    st.markdown("Internal tool for collecting, enriching, and building blockchain transaction data")
    
    # Sidebar - DB Viewer controls
    with st.sidebar:
        st.header("Database Explorer")
        tables = get_mock_db_tables()
        selected_table = st.selectbox("Select Table:", tables, index=tables.index(st.session_state.selected_table))
        st.session_state.selected_table = selected_table
        
        st.divider()
        st.subheader("Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Transactions", f"{random.randint(1000, 9999):,}")
            st.metric("Blocks", f"{random.randint(10000, 99999):,}")
        with col2:
            st.metric("Entities", f"{random.randint(500, 2000):,}")
            st.metric("Addresses", f"{random.randint(2000, 5000):,}")
        
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
    
    # Main content - Three-legged process
    col1, col2 = st.columns([2, 3])
    
    # Left column - Process controls
    with col1:
        st.subheader("Process Controls")
        
        # 1. Collect stage
        with st.expander("1. Collector", expanded=True):
            render_status_indicator(st.session_state.collect_status, "Collector")
            
            # Source selection
            sources = ["Ethereum", "Polygon", "Arbitrum", "All Chains"]
            selected_sources = st.multiselect("Data Sources:", sources, default=["Ethereum"])
            
            time_range = st.select_slider(
                "Time Range:",
                options=["Last hour", "Last 24 hours", "Last week", "Last month", "Custom"]
            )
            
            if time_range == "Custom":
                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input("Start Date")
                with col2:
                    end_date = st.date_input("End Date")
            
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
        
        # 2. Enrich stage
        with st.expander("2. Enricher", expanded=True):
            render_status_indicator(st.session_state.enrich_status, "Enricher")
            
            # Enrichment options
            enrichment_options = [
                "Address Labeling", 
                "Contract Resolution", 
                "Token Data", 
                "Protocol Identification"
            ]
            selected_enrichments = st.multiselect(
                "Enrichment Options:", 
                enrichment_options,
                default=enrichment_options[:2]
            )
            
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
        
        # 3. Build stage
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
    
    # Right column - DB Viewer
    with col2:
        render_db_viewer(st.session_state.selected_table)
    
    # Auto-increment progress for running processes (for demo purposes)
    if st.session_state.collect_status == "running" and st.session_state.progress["collect"] < 1.0:
        st.session_state.progress["collect"] += 0.1
        if st.session_state.progress["collect"] >= 1.0:
            st.session_state.collect_status = "completed"
            st.session_state.progress["collect"] = 1.0
        time.sleep(0.1)
        st.rerun()
    
    if st.session_state.enrich_status == "running" and st.session_state.progress["enrich"] < 1.0:
        st.session_state.progress["enrich"] += 0.08
        if st.session_state.progress["enrich"] >= 1.0:
            st.session_state.enrich_status = "completed"
            st.session_state.progress["enrich"] = 1.0
        time.sleep(0.1)
        st.rerun()
    
    if st.session_state.build_status == "running" and st.session_state.progress["build"] < 1.0:
        st.session_state.progress["build"] += 0.05
        if st.session_state.progress["build"] >= 1.0:
            st.session_state.build_status = "completed"
            st.session_state.progress["build"] = 1.0
        time.sleep(0.1)
        st.rerun()


if __name__ == "__main__":
    app()
