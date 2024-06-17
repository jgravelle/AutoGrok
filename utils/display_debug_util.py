# display_debug_util.py

import streamlit as st

from base_models.agent_base_model import AgentBaseModel
from base_models.tool_base_model import ToolBaseModel
from base_models.project_base_model import ProjectBaseModel
from base_models.workflow_base_model import WorkflowBaseModel

from configs.config_local import DEBUG


def display_debug():
    if DEBUG:
        st.write("Debug Information")
        
    # Iterate over all session state variables
    for key, value in st.session_state.items():
        
        # Check if the value is an instance of specific classes
        if isinstance(value, (ProjectBaseModel, WorkflowBaseModel, AgentBaseModel, ToolBaseModel)):
            # Display the properties and values of the object
            for prop, prop_value in value.__dict__.items():
                st.write(f"{prop}: {prop_value}")
        else:
            # Display the value directly
            st.write(f"{key}:\n\r {value}")
        
        st.write("---")