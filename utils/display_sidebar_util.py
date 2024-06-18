# display_sidebar_util.py

import importlib
import yaml
import streamlit as st

from configs.config_local import DEBUG

def handle_sidebar_prompt_reengineer():
    if DEBUG:
        print("handle_sidebar_prompt_reengineer()")
    user_request = st.session_state.sidebar_prompt_input.strip()
    if user_request:
        # Load the rephrase_prompt from the file
        with open("prompts/rephrase_prompt.yaml", "r") as file:
            prompt_data = yaml.safe_load(file)
            rephrase_prompt = prompt_data["rephrase_prompt"]

        # Dynamically import the provider class based on the selected provider name
        provider_module = importlib.import_module(f"providers.{st.session_state.default_provider.lower()}")
        provider_class = getattr(provider_module, st.session_state.default_provider)
        provider = provider_class(api_url="", api_key=st.session_state.default_provider_key)
        model = st.session_state.selected_model

        try:
            # Replace '{user_request}' in rephrase_prompt with the actual user's request
            formatted_prompt = rephrase_prompt.replace("{user_request}", user_request)
            if DEBUG:
                print(f"Formatted prompt: {formatted_prompt}")
            # Send the formatted prompt to the provider
            response = provider.send_request({"model": model, "messages": [{"role": "user", "content": formatted_prompt}]})
            rephrased_request = provider.process_response(response)["choices"][0]["message"]["content"]
            
            # Update the session state with the rephrased request
            st.session_state.sidebar_prompt_output = rephrased_request
        except Exception as e:
            st.sidebar.error(f"Error processing the request: {str(e)}")

def display_sidebar_prompt_reengineer():
    if DEBUG:
        print("display_sidebar_prompt_reengineer()")

    st.sidebar.write("<div class='title'>AutoGrok™ <br/> Universal AI Agents Made Easy. <br/> Eventually.</div><p/>", unsafe_allow_html=True)
    st.sidebar.write("(We're putting the 'mental' in 'experimental'.)")
    st.sidebar.write("No need to report what's broken, we know.")
    
    # Create the input field in the sidebar
    st.sidebar.text_area("Quickstart - Enter your project request:", key="sidebar_prompt_input", on_change=handle_sidebar_prompt_reengineer)

    # Display the rephrased request if available
    if "sidebar_prompt_output" in st.session_state:
        st.sidebar.text_area("Rephrased Request:", value=st.session_state.sidebar_prompt_output, height=200)