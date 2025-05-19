"""UI components for the Fast & Dirty Commit app."""

from fdc.ui.components import (
    render_status_indicator,
    render_process_controls,
    render_db_viewer
)

from fdc.ui.sidebar import render_sidebar
from fdc.ui.stages import (
    render_collector_stage,
    render_enricher_stage,
    render_builder_stage
)
from fdc.ui.auto_progress import update_progress

__all__ = [
    'render_status_indicator',
    'render_process_controls',
    'render_db_viewer',
    'render_sidebar',
    'render_collector_stage',
    'render_enricher_stage',
    'render_builder_stage',
    'update_progress'
]
