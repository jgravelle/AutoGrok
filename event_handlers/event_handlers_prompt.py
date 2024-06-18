# event_handlers_prompt.py

import importlib
import streamlit as st
import yaml

from configs.config_local import DEBUG

def handle_prompt(user_request, prompt_file_path, prompt_label):
    if DEBUG:
        print(f"handle_prompt()\n\r - User request: {user_request}\n\r Prompt file path: {prompt_file_path}\n\r Prompt label: {prompt_label}")
    if user_request:
        # Load the prompt from the file
        with open(prompt_file_path, "r") as file:
            prompt_data = yaml.safe_load(file)
            prompt = prompt_data[prompt_label]

        # Dynamically import the provider class based on the selected provider name
        provider_module = importlib.import_module(f"providers.{st.session_state.default_provider.lower()}")
        provider_class = getattr(provider_module, st.session_state.default_provider)
        provider = provider_class(api_url="", api_key=st.session_state.default_provider_key)
        model = st.session_state.selected_model

        try:
            # Replace '{user_request}' in the prompt with the actual user's request
            formatted_prompt = prompt.replace("{user_request}", user_request)
            if DEBUG:
                print(f"Formatted prompt: {formatted_prompt}")
            # Send the formatted prompt to the provider
            response = provider.send_request({"model": model, "messages": [{"role": "user", "content": formatted_prompt}]})
            result_text = provider.process_response(response)["choices"][0]["message"]["content"]
            return result_text
        except Exception as e:
            st.error(f"Error processing the request: {str(e)}")
    return None

