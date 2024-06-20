# event_handlers_agent.py

import importlib
import re
import streamlit as st
import yaml

from datetime import datetime
from base_models.agent_base_model import AgentBaseModel
from configs.config_local import DEBUG


def handle_agent_close():
    if DEBUG:
        print("handle_agent_close()")
    st.session_state.current_agent = None
    st.session_state.agent_dropdown = "Select..."
    # st.rerun()


def handle_ai_agent_creation():
    if DEBUG:
        print("handle_ai_agent_creation()")
    agent_creation_input = st.session_state.agent_creation_input.strip()
    if agent_creation_input:
        # Load the generate_agent_prompt from the file
        with open("prompts/generate_agent_prompt.yaml", "r") as file:
            prompt_data = yaml.safe_load(file)
            if prompt_data is not None and "generate_agent_prompt" in prompt_data:
                generate_agent_prompt = prompt_data["generate_agent_prompt"]
            else:
                st.error("Failed to load the agent prompt.")
                return

        # Combine the generate_agent_prompt with the user input
        prompt = f"{generate_agent_prompt}\n\nRephrased agent request: {agent_creation_input}"

        # Dynamically import the provider class based on the selected provider name
        provider_module = importlib.import_module(f"providers.{st.session_state.default_provider.lower()}")
        provider_class = getattr(provider_module, st.session_state.default_provider)
        provider = provider_class(api_url="", api_key=st.session_state.default_provider_key)
        model = st.session_state.selected_model

        try:
            response = provider.send_request({"model": model, "messages": [{"role": "user", "content": prompt}]})
            agent_code = provider.process_response(response)["choices"][0]["message"]["content"]

            # Extract the agent name from the generated code
            agent_name_match = re.search(r"# Agent filename: (\w+)\.py", agent_code)
            if agent_name_match:
                agent_name = agent_name_match.group(1)
            else:
                class_name_match = re.search(r"class (\w+):", agent_code)
                if class_name_match:
                    agent_name = class_name_match.group(1)
                else:
                    st.error("Failed to extract the agent name or class name from the generated code.")
                    return

            agent_data = {
                "name": agent_name,
                "config": {"name": agent_name},
                "skills": [],
                "code": agent_code
            }
            agent = AgentBaseModel.create_agent(agent_name, agent_data)
            st.session_state.current_agent = agent
            st.session_state.agent_dropdown = agent_name
            st.success(f"Agent '{agent_name}' created successfully!")
        except Exception as e:
            st.error(f"Error generating the agent: {str(e)}")


def handle_agent_property_change():
    if DEBUG:
        print("handle_agent_property_change()")
    agent = st.session_state.current_agent
    if agent:
        agent.name = st.session_state.current_agent.name
        agent.description = st.session_state.current_agent.description
        agent.role = st.session_state.current_agent.role
        agent.goal = st.session_state.current_agent.goal
        agent.backstory = st.session_state.current_agent.backstory

        agent_data = agent.to_dict()
        agent_name = agent.name
        with open(f"agents/{agent_name}.yaml", "w") as file:
            yaml.dump(agent_data, file)


def handle_agent_selection():
    if DEBUG:
        print("handle_agent_selection()")
    selected_agent = st.session_state.agent_dropdown
    if selected_agent == "Select...":
        return
    if selected_agent == "Create manually...":
        # Handle manual agent creation
        agent_name = st.session_state.agent_name_input.strip()
        if agent_name:
            agent_data = {
                "name": agent_name,
                "description": "",
                "role": "",
                "goal": "",
                "backstory": "",
                "tools": [],
                "config": {},
                "timestamp": datetime.now().isoformat(),
                "user_id": "default"
            }
            agent = AgentBaseModel.from_dict(agent_data)
            AgentBaseModel.create_agent(agent_name, agent)
            st.session_state.current_agent = agent
            st.session_state.agent_dropdown = agent_name    
    elif selected_agent == "Create with AI...":
        # Clear the current agent selection
        st.session_state.current_agent = None
    else:
        # Load the selected agent
        agent = AgentBaseModel.get_agent(selected_agent)
        st.session_state.current_agent = agent


def handle_agent_name_change():
    if DEBUG:
        print("handle_agent_name_change()")
    new_agent_name = st.session_state.agent_name_edit.strip()
    if new_agent_name:
        st.session_state.current_agent.name = new_agent_name
        update_agent()


def update_agent():
    if DEBUG:
        print("update_agent()")
    st.session_state.current_agent.updated_at = datetime.now().isoformat()
    agent_name = st.session_state.current_agent.name
    agent_data = st.session_state.current_agent.to_dict()
    with open(f"agents/{agent_name}.yaml", "w") as file:
        yaml.dump(agent_data, file)