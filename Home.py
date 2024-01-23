import streamlit as st
import subprocess
import sys
import os

def update_script():
    try:
        # Get the script's directory
        script_directory = os.path.dirname(os.path.realpath(__file__))

        # Set the working directory to the script's directory
        os.chdir(script_directory)

        # Run git fetch to update remote branches
        subprocess.run(['git', 'fetch'])

        # Check if there are any changes
        result = subprocess.run(['git', 'status', '-uno'], capture_output=True, text=True)

        if "Your branch is behind" in result.stdout:
            print("Updating script...")
            subprocess.run(['git', 'pull'])
            print("Script updated. Please restart the script.")
            sys.exit(0)
        else:
            print("Your script is up to date.")

    except Exception as e:
        print(f"Error updating script: {e}")

# Call the function to update the script
update_script()


st.set_page_config(
    page_title="Auto WhatApper - Home",
    page_icon="💬",
)

st.write("# Welcome to Auto WhatApper!")
# add linkedin link for Yedidya Harris
st.markdown('#### By [Yedidya Harris](https://www.linkedin.com/in/yedidya-harris/)')

st.sidebar.success("Select an option above.")

# instructions, in this app you can send messages to phone numbers or to contacts/groups
st.write("### Instructions:")
st.write('Choose an option from the sidebar on the left.')


