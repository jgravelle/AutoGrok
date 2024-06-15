# openai_provider.py

import json
import os
import requests
import streamlit as st

from configs.config_local import DEBUG
from providers.base_provider import BaseLLMProvider

class Openai_Provider(BaseLLMProvider):
    def __init__(self, api_url, api_key):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.api_url = "https://api.openai.com/v1/chat/completions"


    def get_available_models(self):
        if DEBUG:
            print ("GROQ: get_available_models")
            print (f"KEY: {self.api_key}")
        response = requests.get("https://api.openai.com/v1/models", headers={
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
        print("self.api_url: ", self.api_url)
        
        # Check for API key in environment variable
        api_key = os.environ.get("OPENAI_API_KEY")
        
        # If not found in environment variable, check session state
        if not api_key:
            api_key = st.session_state.get("default_provider_key")
        
        # If not found in session state, check global variable
        if not api_key:
            api_key = globals().get("OPENAI_API_KEY")
        
        # If no API key is found, raise an exception
        if not api_key:
            raise Exception("No OpenAI API key found. Please provide an API key.")
        
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
        print("response.status_code: ", response.status_code)
        print("response.text: ", response.text)
        return response
    