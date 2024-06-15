# main.py

import streamlit as st

from base_models.project_base_model import ProjectBaseModel
from session_variables import initialize_session_variables
from utils.display_util import sidebar_begin, display_main


def main():
    st.set_page_config(page_title="AutoGrok™")
    initialize_session_variables()
    sidebar_begin()
    
    # Main content area
    display_main()


if __name__ == "__main__":
    main()