# event_handlers_tool.py

import importlib
import re
import streamlit as st
import yaml

from datetime import datetime
from base_models.tool_base_model import ToolBaseModel
from configs.config_local import DEBUG


def handle_ai_tool_creation():
    if DEBUG:
        print("handle_ai_tool_creation()")
    tool_creation_input = st.session_state.tool_creation_input.strip()
    if tool_creation_input:
        # Load the generate_tool_prompt from the file
        with open("prompts/generate_tool_prompt.yaml", "r") as file:
            prompt_data = yaml.safe_load(file)
            generate_tool_prompt = prompt_data["generate_tool_prompt"]

        # Combine the generate_tool_prompt with the user input
        prompt = f"{generate_tool_prompt}\n\nRephrased tool request: {tool_creation_input}"

        # Dynamically import the provider class based on the selected provider name
        provider_module = importlib.import_module(f"providers.{st.session_state.default_provider.lower()}")
        provider_class = getattr(provider_module, st.session_state.default_provider)
        provider = provider_class(api_url="", api_key=st.session_state.default_provider_key)
        model = st.session_state.selected_model

        try:
            response = provider.send_request({"model": model, "messages": [{"role": "user", "content": prompt}]})
            tool_code = provider.process_response(response)["choices"][0]["message"]["content"]

            # Extract the tool name from the generated code
            tool_name_match = re.search(r"# Tool filename: ([\w_]+)\.py", tool_code)
            if tool_name_match:
                tool_name = tool_name_match.group(1)
                tool_data = {
                    "name": tool_name,
                    "title": tool_name,
                    "content": tool_code,
                    "file_name": f"{tool_name}.json",
                    "description": None,
                    "timestamp": datetime.now().isoformat(),
                    "user_id": "default"
                }
                tool = ToolBaseModel.create_tool(tool_name, tool_data)
                st.session_state.current_tool = tool
                st.session_state.tool_dropdown = tool_name
                st.success(f"Tool '{tool_name}' created successfully!")
            else:
                st.error("Failed to extract the tool name from the generated code.")
        except Exception as e:
            st.error(f"Error generating the tool: {str(e)}")


def handle_tool_close():
    if DEBUG:
        print("handle_tool_close()")
    st.session_state.current_tool = None
    st.session_state.tool_dropdown = "Select..."
    # st.rerun()


def handle_tool_property_change():
    if DEBUG:
        print("handle_tool_property_change()")
    tool = st.session_state.current_tool
    if tool:
        tool.name = st.session_state[f"tool_name_{tool.name}"]
        tool.title = st.session_state[f"tool_title_{tool.name}"]
        tool.description = st.session_state[f"tool_description_{tool.name}"]
        tool.file_name = st.session_state[f"tool_file_name_{tool.name}"]
        tool.content = st.session_state[f"tool_content_{tool.name}"]
        tool.user_id = st.session_state[f"tool_user_id_{tool.name}"]

        tool_data = tool.to_dict()
        tool_name = tool.name
        with open(f"tools/yaml/{tool_name}.yaml", "w") as file:
            yaml.dump(tool_data, file)


def handle_tool_selection():
    if DEBUG:
        print("handle_tool_selection()")
    selected_tool = st.session_state.tool_dropdown
    if selected_tool     == "Select...":
        return
    if selected_tool == "Create manually...":
        # Handle manual tool creation
        tool_name = st.session_state.tool_name_input.strip()
        if tool_name:
            tool_data = {
                "name": tool_name,
                "title": tool_name,
                "content": "",
                "file_name": f"{tool_name}.json",
                "description": None,
                "timestamp": datetime.now().isoformat(),
                "user_id": "default"
            }
            tool = ToolBaseModel.create_tool(tool_name, tool_data)
            st.session_state.current_tool = tool
            st.session_state.tool_dropdown = tool_name
    elif selected_tool == "Create with AI...":
        # Clear the current tool selection
        st.session_state.current_tool = None
    else:
        # Load the selected tool
        tool = ToolBaseModel.get_tool(selected_tool)
        st.session_state.current_tool = tool


def handle_tool_name_change():
    if DEBUG:
        print("handle_tool_name_change()")
    new_tool_name = st.session_state.tool_name_edit.strip()
    if new_tool_name:
        st.session_state.current_tool.name = new_tool_name
        update_tool()


def update_tool():
    if DEBUG:
        print("update_tool()")
    st.session_state.current_tool.updated_at = datetime.now().isoformat()
    tool_name = st.session_state.current_tool.name
    tool_data = st.session_state.current_tool.to_dict()
    with open(f"tools/yaml/{tool_name}.yaml", "w") as file:
        yaml.dump(tool_data, file)