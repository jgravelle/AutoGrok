# display_settings_util.py

import importlib
import os
import streamlit as st

from configs.config_local import DEBUG, DEFAULT_MODEL
from event_handlers.event_handlers_settings import handle_default_provider_change, load_provider_classes

def display_settings():
    if DEBUG:
        print("display_settings()")

    st.write("Settings")
    provider_classes = load_provider_classes()
    default_provider = st.session_state.default_provider if st.session_state.default_provider else ""
    default_provider_index = provider_classes.index(default_provider) if default_provider in provider_classes else 0
    selected_provider = st.selectbox("Default Provider", provider_classes, index=default_provider_index, key="default_provider", on_change=handle_default_provider_change)

    if selected_provider:
        tmp = "_Provider"
        api_key = st.text_input("Default Provider's API Key:", type="password")
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

                # Set the default model selection
                default_model = DEFAULT_MODEL  # Replace with your desired default model
                if default_model in available_models:
                    default_index = available_models.index(default_model)
                else:
                    default_index = 0

                selected_model = st.selectbox("Select Default Model", available_models, index=default_index)
                st.session_state.selected_model = selected_model
            except Exception as e:
                st.error(f"Error retrieving available models: {str(e)}")

    st.session_state.current_framework = st.selectbox("Default Framework", ["Autogen", "CrewAI", "Bob's Agent Maker", "AI-Mart", "Geeks'R'Us"], key="default_framework")