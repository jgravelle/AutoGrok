# display_debug_util.py

import streamlit as st
import yaml

from base_models.agent_base_model import AgentBaseModel
from base_models.tool_base_model import ToolBaseModel
from base_models.project_base_model import ProjectBaseModel
from base_models.workflow_base_model import WorkflowBaseModel

from configs.config_local import DEBUG


def display_debug():
    if DEBUG:
        st.write("Debug Information")
        
        # Create expanders for each object type
        project_expander = st.expander("Project")
        workflow_expander = st.expander("Workflow")
        agent_expander = st.expander("Agent")
        tool_expander = st.expander("Tool")
        other_expander = st.expander("Other")
        
        # Iterate over all session state variables
        for key, value in st.session_state.items():
            
            # Check if the value is an instance of specific classes
            if isinstance(value, ProjectBaseModel):
                with project_expander:
                    st.write(f"### {key}")
                    col1, col2 = st.columns(2)
                    with col1:
                        for prop, prop_value in value.__dict__.items():
                            st.write(f"- **{prop}:** {prop_value}")
                    with col2:
                        st.write(f"```yaml\n{yaml.dump(value.to_dict())}\n```")
                        
            elif isinstance(value, WorkflowBaseModel):
                with workflow_expander:
                    st.write(f"### {key}")
                    col1, col2 = st.columns(2)
                    with col1:
                        for prop, prop_value in value.__dict__.items():
                            st.write(f"- **{prop}:** {prop_value}")
                    with col2:
                        st.write(f"```yaml\n{yaml.dump(value.to_dict())}\n```")
                        
            elif isinstance(value, AgentBaseModel):
                with agent_expander:
                    st.write(f"### {key}")
                    col1, col2 = st.columns(2)
                    with col1:
                        for prop, prop_value in value.__dict__.items():
                            st.write(f"- **{prop}:** {prop_value}")
                    with col2:
                        st.write(f"```yaml\n{yaml.dump(value.to_dict())}\n```")
                        
            elif isinstance(value, ToolBaseModel):
                with tool_expander:
                    st.write(f"### {key}")
                    col1, col2 = st.columns(2)
                    with col1:
                        for prop, prop_value in value.__dict__.items():
                            st.write(f"- **{prop}:** {prop_value}")
                    with col2:
                        st.write(f"```yaml\n{yaml.dump(value.to_dict())}\n```")
                        
            else:
                with other_expander:
                    st.write(f"### {key}")
                    st.write(f"```\n{value}\n```")