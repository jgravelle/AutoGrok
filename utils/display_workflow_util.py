# display_workflow_util.py

import streamlit as st

from base_models.workflow_base_model import WorkflowBaseModel
from configs.config_local import DEBUG
from datetime import datetime

from event_handlers.event_handlers_workflow import (
    handle_workflow_close, handle_workflow_description_change, 
    handle_workflow_name_change, handle_workflow_selection, handle_workflow_summary_method_change,
    handle_workflow_type_change
)   


def display_workflow_dropdown():
    if DEBUG:
        print("display_workflow_dropdown()")
    if st.session_state.current_workflow is None:
        # Display the workflows dropdown
        workflow_names = WorkflowBaseModel.load_workflows()
        selected_workflow = st.selectbox(
            "Workflows",
            ["Select..."] + ["Create..."] + workflow_names,
            key="workflow_dropdown",
            on_change=handle_workflow_selection,
        )
        if selected_workflow == "Select...":
            return
        if selected_workflow == "Create...":
            # Show the create workflow input field
            st.text_input("Workflow Name:", key="workflow_name_input", on_change=handle_workflow_selection)
    else:
        st.session_state.current_workflow.name = st.text_input(
            "Workflow Name:",
            value=st.session_state.current_workflow.name,
            key="workflow_name_edit",
            on_change=handle_workflow_name_change,
        )
        if st.button("CLOSE THIS WORKFLOW"):
            handle_workflow_close()


def display_workflow_properties(workflow):
    # Display the properties of the current workflow
    if st.session_state.current_workflow is not None:
        workflow = st.session_state.current_workflow
        st.write(f"Name: {workflow.name}")
        workflow.description = st.text_area("Description:", value=workflow.description or "", key="tab2_workflow_description", on_change=handle_workflow_description_change)
        workflow.type = st.text_input("Type:", value=workflow.type, key="tab2_workflow_type", on_change=handle_workflow_type_change)
        workflow.summary_method = st.text_input("Summary Method:", value=workflow.summary_method, key="tab2_workflow_summary_method", on_change=handle_workflow_summary_method_change)

        # Add more workflow properties as needed

        # Display agent children
        st.write("Agents:")
        for agent_name, agent in workflow.agent_children.items():
            st.write(f"- {agent_name}")

        with st.container(border=True):
            st.write("Sender:")
            st.write(f"Type: {workflow.sender.type}")
            st.write(f"User ID: {workflow.sender.user_id}")

        with st.container(border=True):
            st.write("Receiver:")
            st.write(f"Type: {workflow.receiver.type}")
            st.write(f"User ID: {workflow.receiver.user_id}")


def display_workflow_timestamps(workflow):
    if st.session_state.current_workflow is not None:
        st.write("<div style='color:#33FFFC; font-weight:bold; text-align:right; width:100%;'>WORKFLOW PROPERTIES</div>", unsafe_allow_html=True)
        if workflow.created_at:
            created_at = datetime.fromisoformat(workflow.created_at).strftime("%B %d, %Y %I:%M %p")
            st.write(f"<div style='text-align:right; width:100%;'>Created At: {created_at}</div>", unsafe_allow_html=True)
        if workflow.updated_at:
            updated_at = datetime.fromisoformat(workflow.updated_at).strftime("%B %d, %Y %I:%M %p")
            st.write(f"<div style='text-align:right; width:100%;'>Updated At: {updated_at}</div>", unsafe_allow_html=True)
