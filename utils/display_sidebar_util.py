# display_sidebar_util.py

import streamlit as st

from base_models.project_base_model import ProjectBaseModel
from configs.config_local import DEBUG
from event_handlers.event_handlers_prompt import handle_prompt


def display_sidebar_message():
    if DEBUG:
        print("display_sidebar_message()")
    st.sidebar.write("<div class='teeny'>Need agents right frickin' now? : <a href='https://autogroq.streamlit.app/'>https://autogroq.streamlit.app/</a></div><p/>", unsafe_allow_html=True)
    st.sidebar.write("<div class='title'>AutoGrok™ <br/> </div>", unsafe_allow_html=True)
    st.sidebar.write("<div class='teeny'>Universal AI Agents Made Easy. <br/> Theoretically.</div><p/>", unsafe_allow_html=True)
    st.sidebar.write("<div class='teeny'>We're putting the 'mental' in 'experimental'.</div>", unsafe_allow_html=True)
    st.sidebar.write("<div class='teeny'>No need to report what's broken, we know.</div><p/><br/><p/>", unsafe_allow_html=True)


def display_sidebar_prompt_reengineer():
    if DEBUG:
        print("display_sidebar_prompt_reengineer()")
    
    # Create the input field in the sidebar
    st.sidebar.text_area("Quickstart - Enter your project request:", key="sidebar_prompt_input", on_change=(handle_sidebar_prompt_reengineer))

    # Display the rephrased request if available
    if "sidebar_prompt_output" in st.session_state:
        st.sidebar.text_area("Rephrased Request:", value=st.session_state.sidebar_prompt_output, height=200)

def handle_sidebar_prompt_reengineer():
    if DEBUG:
        print("handle_sidebar_prompt_reengineer()")
    user_request = st.session_state.sidebar_prompt_input.strip()
    result_text = handle_prompt(user_request, "prompts/rephrase_prompt.yaml", "rephrase_prompt")
    if result_text:
        st.session_state.sidebar_prompt_output = result_text
        # Create new Project named "New Project" with the rephrased request as the 'prompt' property value
        st.session_state.current_project = ProjectBaseModel(name="New Project", prompt=result_text)
        st.session_state.current_project.create_project("New Project")
        st.session_state.current_project.set_prompt(result_text)
