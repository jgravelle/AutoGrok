# display_util.py

import importlib
import os
import streamlit as st

from base_models.agent_base_model import AgentBaseModel
from base_models.tool_base_model import ToolBaseModel
from base_models.project_base_model import (
    ProjectBaseModel, ProjectPriority, ProjectStatus,
)
from base_models.workflow_base_model import WorkflowBaseModel
from configs.config_local import DEBUG
from datetime import datetime
from event_handlers.event_handlers_agent import (
    handle_agent_selection, handle_ai_agent_creation, handle_agent_property_change
    )
from event_handlers.event_handlers_project import (
    handle_project_collaborators_change, handle_project_close, 
    handle_project_description_change, handle_project_due_date_change, 
    handle_project_name_change, handle_project_notes_change, 
    handle_project_selection, handle_project_status_change, handle_project_user_id_change, 
    handle_prompt_change
)
from event_handlers.event_handlers_settings import handle_default_provider_change, load_provider_classes
from event_handlers.event_handlers_tool import (
    handle_ai_tool_creation, handle_tool_property_change, handle_tool_selection, 
)
from event_handlers.event_handlers_workflow import (
    handle_workflow_close, handle_workflow_description_change, 
    handle_workflow_name_change, handle_workflow_selection, handle_workflow_summary_method_change,
    handle_workflow_type_change
)   
from providers.groq_provider import Groq_Provider
from providers.openai_provider import Openai_Provider


def display_main():
    if DEBUG:
        print("called display_main()")
    
    with open("styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    projectTab, workflowTab, agentTab, toolTab, settingsTab, debugTab = st.tabs(["Project", "Workflows", "Agents", "Tools", "Settings", "Debug"])

    with projectTab:
        col1, col2 = st.columns(2)
        with col1:
            display_project_dropdown()
                
        with col2:
            if st.session_state.current_project is not None:
                project = st.session_state.current_project
                st.write("<div class='project-properties'>PROJECT PROPERTIES</div>", unsafe_allow_html=True)
                if project.created_at:
                    created_at = datetime.fromisoformat(project.created_at).strftime("%B %d, %Y %I:%M %p")
                    st.write(f"<div class='timestamp'>Created At: {created_at}</div>", unsafe_allow_html=True)
                if project.updated_at:
                    updated_at = datetime.fromisoformat(project.updated_at).strftime("%B %d, %Y %I:%M %p")
                    st.write(f"<div class='timestamp'>Updated At: {updated_at}</div>", unsafe_allow_html=True)  

        # Display the properties of the current project
        if st.session_state.current_project is not None:
            # Display the name of the first element in the project.workflows array
            if len(st.session_state.current_project.workflows) > 0:
                workflow = st.session_state.current_project.workflows[0]
                st.write(f"<div class='workflow-name'>Workflow: {workflow}</div>", unsafe_allow_html=True)
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


        with workflowTab:
            workflow = st.session_state.current_workflow
            col1, col2 = st.columns(2)
        with col1:
            display_workflow_dropdown()
                           
            with col2:
                if st.session_state.current_workflow is not None:
                    st.write("<div style='color:#33FFFC; font-weight:bold; text-align:right; width:100%;'>WORKFLOW PROPERTIES</div>", unsafe_allow_html=True)
                    if workflow.created_at:
                        created_at = datetime.fromisoformat(workflow.created_at).strftime("%B %d, %Y %I:%M %p")
                        st.write(f"<div style='text-align:right; width:100%;'>Created At: {created_at}</div>", unsafe_allow_html=True)
                    if workflow.updated_at:
                        updated_at = datetime.fromisoformat(workflow.updated_at).strftime("%B %d, %Y %I:%M %p")
                        st.write(f"<div style='text-align:right; width:100%;'>Updated At: {updated_at}</div>", unsafe_allow_html=True)


            # Display the properties of the current workflow
            if st.session_state.current_workflow is not None:
                workflow = st.session_state.current_workflow
                st.write(f"Name: {workflow.name}")
                workflow.description = st.text_area("Description:", value=workflow.description or "", key="tab2_workflow_description", on_change=handle_workflow_description_change)
                workflow.type = st.text_input("Type:", value=workflow.type, key="tab2_workflow_type", on_change=handle_workflow_type_change)
                workflow.summary_method = st.text_input("Summary Method:", value=workflow.summary_method, key="tab2_workflow_summary_method", on_change=handle_workflow_summary_method_change)

                # Add more workflow properties as needed

                # Display agents, sender, and receiver information
                st.write("Agents:")
                for agent in workflow.agents:
                    st.write(f"- {agent.name}")

                with st.container(border=True):
                    st.write("Sender:")
                    st.write(f"Type: {workflow.sender.type}")
                    st.write(f"User ID: {workflow.sender.user_id}")

                with st.container(border=True):
                    st.write("Receiver:")
                    st.write(f"Type: {workflow.receiver.type}")
                    st.write(f"User ID: {workflow.receiver.user_id}")

        with agentTab:
            agent_names = AgentBaseModel.load_agents()
            selected_agent = st.selectbox(
                "Agents",
                ["Select..."] + ["Create manually..."] + ["Create with AI..."] + agent_names,
                key="agent_dropdown",
                on_change=handle_agent_selection,
            )

            if selected_agent == "Create manually...":
                # Show the manual agent creation input field
                st.text_input("Agent Name:", key="agent_name_input", on_change=handle_agent_selection)
            elif selected_agent == "Create with AI...":
                # Show the AI-assisted agent creation input field
                st.text_input("What should this new agent do?", key="agent_creation_input", on_change=handle_ai_agent_creation)

            if st.session_state.current_agent is not None:
                # Display the properties of the current agent
                agent = st.session_state.current_agent
                st.write("<div style='color:#33FFFC; font-weight:bold; text-align:right; width:100%;'>AGENT PROPERTIES</div>", unsafe_allow_html=True)
                st.write(f"<div style='text-align:right; width:100%;'>Timestamp: {agent.timestamp}</div>", unsafe_allow_html=True)

                agent.name = st.text_input("Name:", value=agent.name, key=f"agent_name_{agent.name}", on_change=handle_agent_property_change)
                agent.description = st.text_area("Description:", value=agent.description or "", key=f"agent_description_{agent.name}", on_change=handle_agent_property_change)
                agent.role = st.text_input("Role:", value=agent.role or "", key=f"agent_role_{agent.name}", on_change=handle_agent_property_change)
                agent.goal = st.text_input("Goal:", value=agent.goal or "", key=f"agent_goal_{agent.name}", on_change=handle_agent_property_change)
                agent.backstory = st.text_area("Backstory:", value=agent.backstory or "", key=f"agent_backstory_{agent.name}", on_change=handle_agent_property_change)


        with toolTab:
            tool_names = ToolBaseModel.load_tools()
            selected_tool = st.selectbox(
                "Tools",
                ["Select..."] + ["Create manually..."] + ["Create with AI..."] + tool_names,
                key="tool_dropdown",
                on_change=handle_tool_selection,
            )

            if selected_tool == "Create manually...":
                # Show the manual tool creation input field
                st.text_input("Tool Name:", key="tool_name_input", on_change=handle_tool_selection)
            elif selected_tool == "Create with AI...":
                # Show the AI-assisted tool creation input field
                st.text_input("What should this new tool do?", key="tool_creation_input", on_change=handle_ai_tool_creation)

            if st.session_state.current_tool is not None:
                # Display the properties of the current tool
                tool = st.session_state.current_tool
                st.write("<div style='color:#33FFFC; font-weight:bold; text-align:right; width:100%;'>TOOL PROPERTIES</div>", unsafe_allow_html=True)
                st.write(f"<div style='text-align:right; width:100%;'>Timestamp: {tool.timestamp}</div>", unsafe_allow_html=True)
                
                tool.name = st.text_input("Name:", value=tool.name, key=f"tool_name_{tool.name}", on_change=handle_tool_property_change)
                tool.content = st.text_area("Content:", value=tool.content, key=f"tool_content_{tool.name}", on_change=handle_tool_property_change)
                tool.title = st.text_input("Title:", value=tool.title, key=f"tool_title_{tool.name}", on_change=handle_tool_property_change)
                tool.description = st.text_input("Description:", value=tool.description or "", key=f"tool_description_{tool.name}", on_change=handle_tool_property_change)
                tool.file_name = st.text_input("File Name:", value=tool.file_name, key=f"tool_file_name_{tool.name}", on_change=handle_tool_property_change)
                tool.user_id = st.text_input("User ID:", value=tool.user_id, key=f"tool_user_id_{tool.name}", on_change=handle_tool_property_change)

        with settingsTab:
            st.write("Settings")
            
            provider_classes = load_provider_classes()
            default_provider = st.session_state.default_provider if st.session_state.default_provider else ""
            default_provider_index = provider_classes.index(default_provider) if default_provider in provider_classes else 0
            selected_provider = st.selectbox("Default Provider", provider_classes, index=default_provider_index, key="default_provider", on_change=handle_default_provider_change)

            if selected_provider:
                tmp = "_Provider"
                api_key = st.text_input("API Key:", type="password")
                st.session_state.default_provider_key = api_key

                if st.session_state.default_provider_key or os.environ.get(f"{selected_provider.replace(tmp, '').upper()}_API_KEY"):
                    if os.environ.get(f"{selected_provider.replace(tmp, '').upper()}_API_KEY"):
                        st.session_state.default_provider_key = os.environ.get(f"{selected_provider.replace(tmp, '').upper()}_API_KEY")

                    provider_module = importlib.import_module(f"providers.{selected_provider.lower()}")
                    provider_class = getattr(provider_module, selected_provider)
                    provider = provider_class(api_url="", api_key=st.session_state.default_provider_key)
                    
                    try:
                        if not st.session_state.available_models or len(st.session_state.available_models) == 0:
                            available_models = provider.get_available_models()
                        available_models = sorted(available_models)
                        selected_model = st.selectbox("Select Model", available_models)
                        st.session_state.selected_model = selected_model
                    except Exception as e:
                        st.error(f"Error retrieving available models: {str(e)}")

        with debugTab:
            # Display the debug tab content
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


def display_project_dropdown():
    if DEBUG:
        print("display_project_dropdown()")
    if st.session_state.current_project is None:
        # Display the projects dropdown
        project_names = ProjectBaseModel.load_projects()
        selected_project = st.selectbox(
            "Projects",
            ["Select..."] + ["Create..."] + project_names,
            key="project_dropdown",
            on_change=handle_project_selection,
        )

        if selected_project == "Select...":
            return
        if selected_project == "Create...":
            # Show the create project input field
            st.text_input("Project Name:", key="project_name_input", on_change=handle_project_selection)
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


def sidebar_begin():
    if DEBUG:
        print("sidebar_begin()")

    st.sidebar.title("AutoGrok™")
    # display_project_dropdown()  
    # display_workflow_dropdown()
    