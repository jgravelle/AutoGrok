# display_discussion_util.py

import streamlit as st

from configs.config_local import DEBUG

def display_discussion():
    if DEBUG:
        print("called display_discussion()")
    st.text_area("Agent", height=400)
    st.text_input("User")