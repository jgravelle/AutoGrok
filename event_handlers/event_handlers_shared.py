# event_handlers_shared.py

import json
import streamlit as st
import yaml

from base_models.project_base_model import ProjectBaseModel, WorkflowBaseModel
from configs.config_local import DEBUG
from datetime import datetime



def update_project():
    if DEBUG:
        print("called update_project()")

    # Update the project
    st.session_state.current_project.updated_at = datetime.now().isoformat()
    project_name = st.session_state.current_project.name
    project_data = st.session_state.current_project.to_dict()
    with open(f"projects/yaml/{project_name}.yaml", "w") as file:
        yaml.dump(project_data, file)
    with open(f"projects/json/{project_name}.json", "w") as file:
        json.dump(project_data, file)