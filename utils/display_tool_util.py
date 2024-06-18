# display_tool_util.py

import streamlit as st

from base_models.tool_base_model import ToolBaseModel

from configs.config_local import DEBUG

from event_handlers.event_handlers_tool import (
    handle_ai_tool_creation, handle_tool_close, handle_tool_property_change, handle_tool_selection, 
)


def display_tool_dropdown():
    if DEBUG:
        print("display_tool_dropdown()")
    if st.session_state.current_tool is None:
        # Display the tools dropdown
        tool_names = ToolBaseModel.load_tools()
        selected_tool = st.selectbox(
            "Tools",
            ["Select..."] + ["Create with AI..."] + ["Create manually..."] + tool_names,
            key="tool_dropdown",
            on_change=handle_tool_selection,
        )

        if selected_tool == "Select...":
            return
        if selected_tool == "Create manually...":
            # Show the manual tool creation input field
            st.text_input("Tool Name:", key="tool_name_input", on_change=handle_tool_selection)
        elif selected_tool == "Create with AI...":
            # Show the AI-assisted tool creation input field
            st.text_input("What should this new tool do?", key="tool_creation_input", on_change=handle_ai_tool_creation)
    else:
        st.session_state.current_tool.name = st.text_input(
            "Tool Name:",
            value=st.session_state.current_tool.name,
            key="tool_name_edit",
            on_change=handle_tool_property_change,
        )
        if st.button("CLOSE THIS TOOL"):
            handle_tool_close()


def display_tool_properties():
    if st.session_state.current_tool is not None:
        # Display the properties of the current tool
        tool = st.session_state.current_tool
        st.write("<div style='color:#33FFFC; font-weight:bold; text-align:right; width:100%;'>TOOL PROPERTIES</div>", unsafe_allow_html=True)
        st.write(f"<div style='text-align:right; width:100%;'>Timestamp: {tool.timestamp}</div>", unsafe_allow_html=True)
        
        tool.content = st.text_area("Content:", value=tool.content, key=f"tool_content_{tool.name}", on_change=handle_tool_property_change)
        tool.title = st.text_input("Title:", value=tool.title, key=f"tool_title_{tool.name}", on_change=handle_tool_property_change)
        tool.description = st.text_input("Description:", value=tool.description or "", key=f"tool_description_{tool.name}", on_change=handle_tool_property_change)
        tool.file_name = st.text_input("File Name:", value=tool.file_name, key=f"tool_file_name_{tool.name}", on_change=handle_tool_property_change)
        tool.user_id = st.text_input("User ID:", value=tool.user_id, key=f"tool_user_id_{tool.name}", on_change=handle_tool_property_change)
