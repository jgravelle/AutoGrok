# display_files_util.py

import os
import streamlit as st

from configs.config_local import DEBUG


import os
import streamlit as st

def display_files():
    if DEBUG:
        print("display_files()")

    # Define the folders to display
    folders = ['agents/yaml', 'projects/yaml', 'tools/yaml', 'workflows/yaml']

    # Create a selectbox to choose the folder
    selected_folder = st.selectbox("Select a folder", folders)

    # Get the list of files in the selected folder
    items = os.listdir(selected_folder)
    files = [item for item in items if os.path.isfile(os.path.join(selected_folder, item))]

    if files:
        # Create a selectbox to choose the file
        selected_file = st.selectbox("Select a file", files)

        # Display the content of the selected file
        file_path = os.path.join(selected_folder, selected_file)
        with open(file_path, 'r') as file:
            file_content = file.read()
        st.text_area("File content", file_content, height=400)

        # Add a button to save changes to the file
        if st.button("Save changes"):   
            with open(file_path, 'w') as file:
                file.write(st.session_state.file_content)
            st.success("File saved successfully.")

        # Add a button to delete the file
        if st.button("Delete file"):
            os.remove(file_path)
            st.success("File deleted successfully.")
    else:
        st.warning(f"No files found in the '{selected_folder}' folder.")