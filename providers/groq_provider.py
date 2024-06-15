# groq_provider.py

import json
import os
import requests
import streamlit as st

from configs.config_local import DEBUG
from providers.base_provider import BaseLLMProvider

class Groq_Provider(BaseLLMProvider):
    def __init__(self, api_url, api_key):
        self.api_key = api_key
        if api_url:
            self.api_url = api_url
        else:
            self.api_url = "https://api.groq.com/openai/v1/chat/completions"


    def get_available_models(self):
        if DEBUG:
            print ("GROQ: get_available_models")
            print (f"KEY: {self.api_key}")
        response = requests.get("https://api.groq.com/openai/v1/models", headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })
        if response.status_code == 200:
            models = response.json().get("data", [])
            return [model["id"] for model in models]
        else:
            raise Exception(f"Failed to retrieve models: {response.status_code}")


    def process_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with status code {response.status_code}")


    def send_request(self, data):
        # Check for API key in environment variable
        api_key = os.environ.get("GROQ_API_KEY")
        
        # If not found in environment variable, check session state
        if not api_key:
            api_key = st.session_state.get("default_provider_key")
        
        # If not found in session state, check global variable
        if not api_key:
            api_key = globals().get("GROQ_API_KEY")
        
        # If no API key is found, raise an exception
        if not api_key:
            raise Exception("No Groq API key found. Please provide an API key.")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        # Ensure data is a JSON string
        if isinstance(data, dict):
            json_data = json.dumps(data)
        else:
            json_data = data
        response = requests.post(self.api_url, data=json_data, headers=headers)
        return response
    