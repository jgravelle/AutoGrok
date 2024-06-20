# event_handlers_project.py

import os
import streamlit as st

from base_models.project_base_model import ProjectBaseModel
from base_models.workflow_base_model import WorkflowBaseModel
from configs.config_local import DEBUG
from event_handlers.event_handlers_prompt import handle_prompt
from event_handlers.event_handlers_shared import update_project
from event_handlers.event_handlers_workflow import handle_workflow_close, update_workflow

# def handle_project_attachments_change():
#     new_project_attachments = st.session_state.current_project.attachments.strip()
#     if new_project_attachments:
#         attachments = [attachment.strip() for attachment in new_project_attachments.split(",")]
#         st.session_state.current_project.attachments = attachments
#         update()


def handle_project_collaborators_change():
    if DEBUG:
        print("called handle_project_collaborators_change()")
    new_project_collaborators = st.session_state.project_collaborators.strip()
    if new_project_collaborators:
        collaborators = [collaborator.strip() for collaborator in new_project_collaborators.split(",")]
        st.session_state.current_project.collaborators = collaborators
        update_project()


def handle_project_close():
    if DEBUG:
        print("handle_project_close()")
    st.session_state.current_project = None
    st.session_state.project_dropdown = "Select..."
    
    # Close the current workflow
    handle_workflow_close()
    
    # st.rerun()


def handle_project_delete():
    if DEBUG:
        print("handle_project_delete()")


def handle_project_description_change():
    if DEBUG:
        print("handle_project_description_change")
    new_project_description = st.session_state.project_description.strip()
    if new_project_description:
        st.session_state.current_project.description = new_project_description
        update_project()


def handle_project_due_date_change():
    if DEBUG:
        print("called handle_project_due_date_change()")
    new_project_due_date = st.session_state.project_due_date
    if new_project_due_date:
        st.session_state.current_project.due_date = new_project_due_date.strftime("%Y-%m-%d")
        update_project()


def handle_project_name_change():
    if DEBUG:
        print("called handle_project_name_change()")
    new_project_name = st.session_state.project_name_edit.strip()
    if new_project_name:
        old_project_name = st.session_state.current_project.name
        st.session_state.current_project.name = new_project_name
        
        # Rename the YAML project file
        old_file_path = f"projects/yaml/{old_project_name}.yaml"
        new_file_path = f"projects/yaml/{new_project_name}.yaml"
        os.rename(old_file_path, new_file_path)

        # Rename the JSON project file
        old_file_path = f"projects/json/{old_project_name}.json"
        new_file_path = f"projects/json/{new_project_name}.json"
        os.rename(old_file_path, new_file_path)
        
        update_project()


def handle_project_notes_change():
    if DEBUG:
        print("called handle_project_notes_change()")
    new_project_notes = st.session_state.project_notes.strip()
    if new_project_notes:
        st.session_state.current_project.notes = new_project_notes
        update_project()


def handle_project_prompt_reengineer():
    if DEBUG:
        print("handle_project_prompt_reengineer()")
    user_request = st.session_state.project_prompt_input.strip()
    result_text = handle_prompt(user_request, "prompts/rephrase_prompt.yaml", "rephrase_prompt")
    if result_text:
        st.session_state.project_prompt_output = result_text
        # Create new Project named "New Project" with the rephrased request as the 'prompt' property value
        st.session_state.current_project = ProjectBaseModel(name="New Project", prompt=result_text)
        st.session_state.current_project.create_project("New Project")
        st.session_state.current_project.set_prompt(result_text)
        st.session_state.current_workflow = WorkflowBaseModel(name="New Workflow")
        st.session_state.current_workflow.create_workflow("New Workflow")
        st.session_state.current_workflow.set_description(user_request + "\n\r" + result_text)

        update_project()
        update_workflow()


def handle_project_selection():
    if DEBUG:
        print("called handle_project_selection()")
    selected_project = st.session_state.project_dropdown
    if selected_project == "Select...":
        return
    if selected_project == "Create from AI...":
        return
    if selected_project == "Create manually...":
        project_name = st.session_state.project_name_input.strip()
        if project_name:
            project = ProjectBaseModel(name=project_name)
            st.session_state.current_project = project
            st.session_state.project_dropdown = project_name
            ProjectBaseModel.create_project(st.session_state.current_project.name)
            
            # Close the current workflow
            handle_workflow_close()
    else:
        # Load the selected project
        project = ProjectBaseModel.get_project(selected_project)
        st.session_state.current_project = project

        # Load the workflows for the selected project
        st.session_state.current_project.workflows = project.workflows


def handle_project_status_change():
    if DEBUG:
        print("called handle_project_status_change()")
    new_project_status = st.session_state.project_status
    if new_project_status:
        st.session_state.current_project.status = new_project_status
        update_project()


def handle_project_user_id_change():
    if DEBUG:
        print("called handle_project_user_id_change()")
    new_project_user_id = st.session_state.project_user_id.strip()
    if new_project_user_id:
        st.session_state.current_project.user_id = new_project_user_id
        update_project()
