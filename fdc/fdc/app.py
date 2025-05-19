"""Streamlit app for Fast & Dirty Commit."""

import subprocess
from pathlib import Path

import streamlit as st
from git import Repo


def get_git_repos():
    """Find Git repositories in common locations."""
    # Common locations to check for Git repos
    home_dir = Path.home()
    common_dev_dirs = [
        home_dir / "dev",
        home_dir / "projects",
        home_dir / "code",
        home_dir / "workspace",
        home_dir / "Documents" / "projects",
    ]
    
    repos = []
    
    # Add any repos found in common locations
    for dev_dir in common_dev_dirs:
        if dev_dir.exists():
            for path in dev_dir.iterdir():
                if path.is_dir() and (path / ".git").exists():
                    repos.append(str(path))
    
    return sorted(repos)


def get_repo_status(repo_path):
    """Get the status of a Git repository."""
    try:
        repo = Repo(repo_path)
        
        # Get branch info
        branch = repo.active_branch.name
        
        # Get status
        changed_files = []
        staged_files = []
        untracked_files = []
        
        for item in repo.index.diff(None):
            changed_files.append(item.a_path)
        
        for item in repo.index.diff("HEAD"):
            staged_files.append(item.a_path)
        
        untracked_files = repo.untracked_files
        
        return {
            "branch": branch,
            "changed_files": changed_files,
            "staged_files": staged_files,
            "untracked_files": untracked_files,
            "repo": repo,
        }
    except Exception as e:
        st.error(f"Error getting repo status: {e}")
        return None


def stage_file(repo, file_path):
    """Stage a file in the Git repository."""
    try:
        repo.git.add(file_path)
        return True
    except Exception as e:
        st.error(f"Error staging file: {e}")
        return False


def unstage_file(repo, file_path):
    """Unstage a file in the Git repository."""
    try:
        repo.git.reset(file_path)
        return True
    except Exception as e:
        st.error(f"Error unstaging file: {e}")
        return False


def commit_changes(repo, message):
    """Commit staged changes."""
    try:
        repo.git.commit("-m", message)
        return True
    except Exception as e:
        st.error(f"Error committing changes: {e}")
        return False


def push_changes(repo):
    """Push committed changes to remote."""
    try:
        repo.git.push()
        return True
    except Exception as e:
        st.error(f"Error pushing changes: {e}")
        return False


def app():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="Fast & Dirty Commit",
        page_icon="🚀",
        layout="wide",
    )
    
    st.title("🚀 Fast & Dirty Commit")
    st.markdown("A quick way to commit and serve changes.")
    
    # Repository selection
    repos = get_git_repos()
    
    if not repos:
        st.warning("No Git repositories found in common locations.")
        repo_path = st.text_input("Enter repository path manually:")
        if repo_path and Path(repo_path).exists() and (Path(repo_path) / ".git").exists():
            repos = [repo_path]
        else:
            if repo_path:
                st.error("Invalid repository path or not a Git repository.")
            return
    
    selected_repo = st.selectbox("Select repository", repos)
    
    if not selected_repo:
        return
    
    # Get repository status
    status = get_repo_status(selected_repo)
    
    if not status:
        return
    
    # Display repository info
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Repository Info")
        st.markdown(f"**Path:** {selected_repo}")
        st.markdown(f"**Branch:** {status['branch']}")
    
    # File status and staging
    st.subheader("Files")
    
    # Untracked files
    if status["untracked_files"]:
        st.markdown("### Untracked Files")
        for file in status["untracked_files"]:
            col1, col2 = st.columns([6, 1])
            with col1:
                st.text(file)
            with col2:
                if st.button("Stage", key=f"stage_{file}"):
                    if stage_file(status["repo"], file):
                        st.rerun()
    
    # Changed files
    if status["changed_files"]:
        st.markdown("### Changed Files")
        for file in status["changed_files"]:
            col1, col2 = st.columns([6, 1])
            with col1:
                st.text(file)
            with col2:
                if st.button("Stage", key=f"stage_changed_{file}"):
                    if stage_file(status["repo"], file):
                        st.rerun()
    
    # Staged files
    if status["staged_files"]:
        st.markdown("### Staged Files")
        for file in status["staged_files"]:
            col1, col2 = st.columns([6, 1])
            with col1:
                st.text(file)
            with col2:
                if st.button("Unstage", key=f"unstage_{file}"):
                    if unstage_file(status["repo"], file):
                        st.rerun()
    
    # Commit section
    st.subheader("Commit")
    
    if not status["staged_files"]:
        st.warning("No files staged for commit.")
    else:
        commit_message = st.text_area("Commit message", placeholder="Enter commit message here...")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Commit", disabled=not commit_message):
                if commit_changes(status["repo"], commit_message):
                    st.success("Changes committed successfully!")
                    st.rerun()
        
        with col2:
            if st.button("Commit & Push", disabled=not commit_message):
                if commit_changes(status["repo"], commit_message):
                    if push_changes(status["repo"]):
                        st.success("Changes committed and pushed successfully!")
                        st.rerun()


def run_app(host="0.0.0.0", port=8501):
    """Run the Streamlit app with the given host and port."""
    # Streamlit doesn't easily allow changing the host/port programmatically,
    # so we use the subprocess module to run the streamlit command
    streamlit_cmd = [
        "streamlit", "run",
        __file__,
        "--server.address", host,
        "--server.port", str(port),
        "--server.headless", "true",
        "--browser.serverAddress", "fdc.dev.local",
        "--browser.serverPort", "443",
    ]
    
    subprocess.run(streamlit_cmd)


if __name__ == "__main__":
    app()
