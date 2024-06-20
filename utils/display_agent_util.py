# display_main_util.py

import streamlit as st

from base_models.agent_base_model import AgentBaseModel
from configs.config_local import DEBUG
from event_handlers.event_handlers_agent import (
    handle_agent_close, handle_agent_selection, handle_ai_agent_creation, handle_agent_property_change
)

def display_agent_dropdown():
    if DEBUG:
        print("display_agent_dropdown()")
    if st.session_state.current_agent is None:
        # Display the agents dropdown
        agent_names = AgentBaseModel.load_agents()
        selected_agent = st.selectbox(
            "Agents",
            ["Select..."] + ["Create with AI..."] + ["Create manually..."] + agent_names,
            key="agent_dropdown",
            on_change=handle_agent_selection,
        )

        if selected_agent == "Select...":
            return
        if selected_agent == "Create manually...":
            # Show the manual agent creation input field
            st.text_input("Agent Name:", key="agent_name_input", on_change=handle_agent_selection)
        elif selected_agent == "Create with AI...":
            # Show the AI-assisted agent creation input field
            st.text_input("What should this new agent do?", key="agent_creation_input", on_change=handle_ai_agent_creation)
    else:
        st.session_state.current_agent.name = st.text_input(
            "Agent Name:",
            value=st.session_state.current_agent.name,
            key="agent_name_edit",
            on_change=handle_agent_property_change,
        )
        if st.button("CLOSE THIS AGENT"):
            handle_agent_close()


def display_agent_properties():
    if DEBUG:
        print("display_agent_properties()")
    agent = st.session_state.current_agent
    st.write("<div style='color:#33FFFC; font-weight:bold; text-align:right; width:100%;'>AGENT PROPERTIES</div>", unsafe_allow_html=True)
    st.write(f"<div style='text-align:right; width:100%;'>Timestamp: {agent.timestamp}</div>", unsafe_allow_html=True)

    agent.description = st.text_area("Description:", value=agent.description or "", key=f"agent_description_{agent.name}", on_change=handle_agent_property_change)
    agent.role = st.text_input("Role:", value=agent.role or "", key=f"agent_role_{agent.name}", on_change=handle_agent_property_change)
    agent.goal = st.text_input("Goal:", value=agent.goal or "", key=f"agent_goal_{agent.name}", on_change=handle_agent_property_change)
    agent.backstory = st.text_area("Backstory:", value=agent.backstory or "", key=f"agent_backstory_{agent.name}", on_change=handle_agent_property_change)

def display_sidebar_agents():
    if DEBUG:
        print("display_sidebar_agents()")
    # Display each agent in the sidebar as a button with the agent's name on it
    agent_names = AgentBaseModel.load_agents()
    if agent_names:
        for agent_name in agent_names:
            if st.sidebar.button(agent_name):
                st.write(f"Speaking to agent: {agent_name}")
    
        


