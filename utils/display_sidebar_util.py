# display_sidebar_util.py

import streamlit as st

from configs.config_local import DEBUG
from utils.display_agent_util import display_sidebar_agents

def display_sidebar():
    if DEBUG:
        print("display_sidebar_message()")
  
    st.sidebar.image('gfx/AutoGroqLogo_sm.png')
    display_sidebar_home()
    display_sidebar_agents()

def display_sidebar_home():
    st.sidebar.write("<div class='teeny'>Need agents right frickin' now? : <a href='https://autogroq.streamlit.app/'>https://autogroq.streamlit.app/</a></div><p/>", unsafe_allow_html=True)
    st.sidebar.write("<div class='teeny'>Universal AI Agents Made Easy. <br/> Theoretically.</div><p/>", unsafe_allow_html=True)
    st.sidebar.write("<div class='teeny'>We're putting the 'mental' in 'experimental'.</div>", unsafe_allow_html=True)
    st.sidebar.write("<div class='teeny yellow'>No need to report what's broken, we know.</div><p/><br/><p/>", unsafe_allow_html=True)  
