# session_variables.py

import streamlit as st

from base_models.project_base_model import ProjectBaseModel
from configs.config_local import LLM_PROVIDER

def initialize_session_variables():

    if "available_models" not in st.session_state:
        st.session_state.available_models = []

    if "current_agent" not in st.session_state:
        st.session_state.current_agent = None

    if "current_project" not in st.session_state:
        st.session_state.current_project = None

    if "current_tool" not in st.session_state:
        st.session_state.current_tool = None

    if "current_workflow" not in st.session_state:
        st.session_state.current_workflow = None

    if "default_llm" not in st.session_state:
        st.session_state.default_llm = ""

    if "default_provider" not in st.session_state:
        st.session_state.default_provider = LLM_PROVIDER

    if "default_provider_key" not in st.session_state:
        st.session_state.default_provider_key = None

    if "project_dropdown" not in st.session_state:
        st.session_state.project_dropdown = "Select..."

    if "project_model" not in st.session_state:
        st.session_state.project_model = ProjectBaseModel()
        
    if "project_name_input" not in st.session_state:
        st.session_state.project_name_input = ""

    if "provider" not in st.session_state:
        st.session_state.provider = ""

    if "reengineer" not in st.session_state:
        st.session_state.reengineer = True

    if "tool_name_input" not in st.session_state:
        st.session_state.tool_name_input = ""        

    if "workflow_dropdown" not in st.session_state:
        st.session_state.workflow_dropdown = "Select..."

    if "workflow_name_input" not in st.session_state:
        st.session_state.workflow_name_input = ""