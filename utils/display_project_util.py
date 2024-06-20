# display_project_util.py

import streamlit as st

from base_models.project_base_model import (
    ProjectBaseModel, ProjectPriority, ProjectStatus,
)
from configs.config_local import DEBUG
from datetime import datetime
from event_handlers.event_handlers_project import (
    handle_project_collaborators_change, handle_project_close, handle_project_delete,
    handle_project_description_change, handle_project_due_date_change, 
    handle_project_name_change, handle_project_notes_change, 
    handle_project_selection, handle_project_status_change, handle_project_user_id_change, 
    handle_project_prompt_reengineer
)
from event_handlers.event_handlers_prompt import handle_prompt_change


def display_project_dropdown():
    if DEBUG:
        print("display_project_dropdown()")
    if st.session_state.current_project is None:
        # Display the projects dropdown
        project_names = ProjectBaseModel.load_projects()
        project_names.sort()
        selected_project = st.selectbox(
            "Projects",
            ["Select..."] + ["Create manually..."] + ["Create from AI..."] + project_names,
            key="project_dropdown",
            on_change=handle_project_selection,
        )

        if selected_project == "Select...":
            return
        if selected_project == "Create manually...":
            # Show the create project input field
            st.text_input("Project Name:", key="project_name_input", on_change=handle_project_selection)
        if selected_project == "Create from AI...":
            st.text_area("Enter your project request:", key="project_prompt_input", on_change=(handle_project_prompt_reengineer))
    else:
        # Display the selected project name as an editable text input
        st.session_state.current_project.name = st.text_input(
            "Project Name:",
            value=st.session_state.current_project.name,
            key="project_name_edit",
            on_change=handle_project_name_change,
        )
        if st.button("CLOSE THIS PROJECT"):
            handle_project_close()



def display_project_properties(project):
    if DEBUG:
        print("display_project_properties()")
    # Display the properties of the current project
    if st.session_state.current_project is not None:
        st.write("Workflows:")
        for workflow_name, workflow in project.workflows.items():
            st.write(f"- {workflow_name}")
        project.prompt = st.text_area("Prompt:", value=project.prompt, key="prompt", on_change=handle_prompt_change)
        project.description = st.text_area("Description:", value=project.description or "", key="project_description", on_change=handle_project_description_change)
        status_options = [status.value for status in ProjectStatus]
        project.status = st.selectbox("Status:", options=status_options, index=status_options.index(project.status), key="project_status", on_change=handle_project_status_change)
        
        if project.due_date:
            if isinstance(project.due_date, str):
                due_date_value = datetime.strptime(project.due_date, "%Y-%m-%d").date()
            else:
                due_date_value = project.due_date
        else:
            due_date_value = None
        
        # Display the date input field
        due_date = st.date_input("Due Date:", value=due_date_value, key="project_due_date")
        
        # Update the project's due date if it has changed
        if due_date != due_date_value:
            project.due_date = due_date.strftime("%Y-%m-%d") if due_date else None
            handle_project_due_date_change()
        
        priority_options = [priority.value for priority in ProjectPriority]
        project.priority = st.selectbox("Priority:", options=priority_options, index=priority_options.index(project.priority), key="project_priority", on_change=handle_project_status_change)
        st.write(f"Tags: {', '.join(project.tags)}")
        
        # Add text input field for notes
        project.notes = st.text_area("Notes:", value=project.notes or "", key="project_notes", on_change=handle_project_notes_change)
        collaborators_input = st.text_input("Collaborators:", value=", ".join(project.collaborators), key="project_collaborators", on_change=handle_project_collaborators_change)
        project.collaborators = [collaborator.strip() for collaborator in collaborators_input.split(",")]
        project.user_id = st.text_input("User ID:", value=project.user_id or "", key="project_user_id", on_change=handle_project_user_id_change)

        # st.write("Attachments:")
        # for attachment in project.attachments:
        #     st.write(f"- {attachment}")

        # new_attachment = st.text_input("Add Attachment:", key="project_new_attachment")
        # if new_attachment:
        #     project.attachments.append(new_attachment)
        #     handle_project_attachments_change()

def display_project_timestamps(project):
    if DEBUG:
        print("display_project_timestamps()")
    st.write("<div class='project-properties'>PROJECT PROPERTIES</div>", unsafe_allow_html=True)
    if project.created_at:
        created_at = datetime.fromisoformat(project.created_at).strftime("%B %d, %Y %I:%M %p")
        st.write(f"<div class='timestamp'>Created At: {created_at}</div>", unsafe_allow_html=True)
    if project.updated_at:
        updated_at = datetime.fromisoformat(project.updated_at).strftime("%B %d, %Y %I:%M %p")
        st.write(f"<div class='timestamp'>Updated At: {updated_at}</div>", unsafe_allow_html=True)