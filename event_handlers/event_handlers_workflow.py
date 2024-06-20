# event_handlers_workflow.py

import json
import os
import streamlit as st
import yaml

from datetime import datetime
from base_models.workflow_base_model import WorkflowBaseModel, Sender, Receiver
from configs.config_local import DEBUG
from event_handlers.event_handlers_shared import update_project


def handle_workflow_close():
    if DEBUG:
        print("called handle_workflow_close()")
    st.session_state.current_workflow = None
    st.session_state.workflow_dropdown = "Select..."
    # st.rerun()


def handle_workflow_delete(workflow_file):
    if DEBUG:
        print(f"called handle_workflow_delete({workflow_file})")
    os.remove(workflow_file)
    st.session_state.current_workflow = None
    st.session_state.workflow_dropdown = "Select..."
    st.success(f"Workflow '{workflow_file}' has been deleted.")


def handle_workflow_description_change():
    if DEBUG:
        print("called handle_workflow_description_change()")
    new_workflow_description = st.session_state.workflow_description.strip()
    if new_workflow_description:
        st.session_state.current_workflow.description = new_workflow_description
        update_workflow()


def handle_workflow_name_change():
    if DEBUG:
        print("called handle_workflow_name_change()")
    new_workflow_name = st.session_state.workflow_name_edit.strip()
    if new_workflow_name:
        old_workflow_name = st.session_state.current_workflow.name
        st.session_state.current_workflow.name = new_workflow_name
        
        # Rename the YAML project file
        old_file_path = f"workflows/yaml/{old_workflow_name}.yaml"
        new_file_path = f"workflows/yaml/{new_workflow_name}.yaml"
        os.rename(old_file_path, new_file_path)

        # Rename the JSON project file
        old_file_path = f"workflows/json/{old_workflow_name}.json"
        new_file_path = f"workflows/json/{new_workflow_name}.json"
        os.rename(old_file_path, new_file_path)
        
        # Update the workflow name in current_project.workflows
        if st.session_state.current_project and old_workflow_name in st.session_state.current_project.workflows:
            st.session_state.current_project.workflows[new_workflow_name] = st.session_state.current_project.workflows.pop(old_workflow_name)
            update_project()
        update_workflow()


def handle_workflow_selection():
    if DEBUG:
        print("called handle_workflow_selection()")
    selected_workflow = st.session_state.workflow_dropdown
    if selected_workflow == "Select...":
        return
    if selected_workflow == "Create...":
        workflow_name = st.session_state.workflow_name_input.strip()
        if workflow_name:
            workflow = WorkflowBaseModel(   
                name=workflow_name,
                description="This workflow is used for general purpose tasks.",
                sender=Sender(
                    type="userproxy",
                    config={
                        "name": "userproxy",
                        "llm_config": {
                            "config_list": [
                                {
                                    "user_id": "default",
                                    "timestamp": "2024-03-28T06:34:40.214593",
                                    "model": "gpt-4o",
                                    "base_url": None,
                                    "api_type": None,
                                    "api_version": None,
                                    "description": "OpenAI model configuration"
                                }
                            ],
                            "temperature": 0.1,
                            "cache_seed": None,
                            "timeout": None,
                            "max_tokens": None,
                            "extra_body": None
                        },
                        "human_input_mode": "NEVER",
                        "max_consecutive_auto_reply": 30,
                        "system_message": "You are a helpful assistant.",
                        "is_termination_msg": None,
                        "code_execution_config": {
                            "work_dir": None,
                            "use_docker": False
                        },
                        "default_auto_reply": "TERMINATE",
                        "description": "A user proxy agent that executes code."
                    },
                    timestamp="2024-03-28T06:34:40.214593",
                    user_id="user",
                    tools=[
                        {
                            "title": "fetch_web_content",
                            "content": "...",  # Omitted for brevity
                            "file_name": "fetch_web_content.json",
                            "description": None,
                            "timestamp": "2024-05-14T08:19:12.425322",
                            "user_id": "default"
                        }
                    ]
                ),
                receiver=Receiver(
                    type="assistant",
                    config={
                        "name": "primary_assistant",
                        "llm_config": {
                            "config_list": [
                                {
                                    "user_id": "default",
                                    "timestamp": "2024-05-14T08:19:12.425322",
                                    "model": "gpt-4o",
                                    "base_url": None,
                                    "api_type": None,
                                    "api_version": None,
                                    "description": "OpenAI model configuration"
                                }
                            ],
                            "temperature": 0.1,
                            "cache_seed": None,
                            "timeout": None,
                            "max_tokens": None,
                            "extra_body": None
                        },
                        "human_input_mode": "NEVER",
                        "max_consecutive_auto_reply": 30,
                        "system_message": "...",  # Omitted for brevity
                        "is_termination_msg": None,
                        "code_execution_config": None,
                        "default_auto_reply": "",
                        "description": "A primary assistant agent that writes plans and code to solve tasks."
                    },
                    groupchat_config={},
                    timestamp=datetime.now().isoformat(),
                    user_id="default",
                    tools=[
                        {
                            "title": "fetch_web_content",
                            "content": "...",  # Omitted for brevity
                            "file_name": "fetch_web_content.json",
                            "description": None,
                            "timestamp": "2024-05-14T08:19:12.425322",
                            "user_id": "default"
                        }
                    ],
                    agents=[]
                ),
                type="twoagents",
                user_id="user",
                timestamp=datetime.now().isoformat(),
                summary_method="last"
            )
            st.session_state.current_workflow = workflow
            st.session_state.workflow_dropdown = workflow_name
            WorkflowBaseModel.create_workflow(st.session_state.current_workflow.name)

            # Add the created workflow's name to current_project.workflows
            if st.session_state.current_project:
                st.session_state.current_project.workflows[workflow_name] = workflow
                update_project()
    else:
        print ("Selected workflow: ", selected_workflow)
        workflow = WorkflowBaseModel.get_workflow(selected_workflow)
        st.session_state.current_workflow = workflow

        # Update current_project.workflows to reflect the selected workflow
        if st.session_state.current_project:
            st.session_state.current_project.workflows[selected_workflow] = workflow
            update_project()



def handle_workflow_type_change():
    if DEBUG:
        print("called handle_workflow_type_change()")
    new_workflow_type = st.session_state.workflow_type.strip()
    if new_workflow_type:
        st.session_state.current_workflow.type = new_workflow_type
        update_workflow()


def handle_workflow_summary_method_change():
    if DEBUG:
        print("called handle_workflow_summary_method_change()")
    new_workflow_summary_method = st.session_state.workflow_summary_method.strip()
    if new_workflow_summary_method:
        st.session_state.current_workflow.summary_method = new_workflow_summary_method
        update_workflow()


def update_workflow():
    if DEBUG:
        print("called update_workflow()")
    st.session_state.current_workflow.updated_at = datetime.now().isoformat()
    workflow_name = st.session_state.current_workflow.name
    workflow_data = st.session_state.current_workflow.to_dict()
    with open(f"workflows/yaml/{workflow_name}.yaml", "w") as file:
        yaml.dump(workflow_data, file)
    with open(f"workflows/yaml/{workflow_name}.json", "w") as file:
        json.dump(workflow_data, file)