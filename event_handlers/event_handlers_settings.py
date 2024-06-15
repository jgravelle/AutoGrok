# event_handlers\event_handlers_settings.py

import importlib
import os
import streamlit as st

from configs.config import DEBUG
from providers.base_provider import BaseLLMProvider


def handle_default_provider_change():
    if DEBUG:
        print("handle_default_provider_change()")
    selected_provider = st.session_state.default_provider
    st.session_state.default_provider = selected_provider


def load_model_classes():
    if DEBUG:
        print("load_model_classes()")
    model_classes = []
    models_folder = "models"

    for file_name in os.listdir(models_folder):
        if file_name.endswith(".py") and file_name != "llm_base_model.py":
            module_name = file_name[:-3]  # Remove the ".py" extension
            module = importlib.import_module(f"{models_folder}.{module_name}")

            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, BaseLLMProvider) and attr != BaseLLMProvider:
                    model_classes.append(attr_name)

    return model_classes


def load_provider_classes():
    if DEBUG:
        print("load_provider_classes()")
    provider_classes = []
    providers_folder = "providers"
    
    for file_name in os.listdir(providers_folder):
        if file_name.endswith(".py") and file_name != "base_provider.py":
            module_name = file_name[:-3]  # Remove the ".py" extension
            module = importlib.import_module(f"{providers_folder}.{module_name}")
            
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, BaseLLMProvider) and attr != BaseLLMProvider:
                    provider_classes.append(attr_name)
    
    return provider_classes