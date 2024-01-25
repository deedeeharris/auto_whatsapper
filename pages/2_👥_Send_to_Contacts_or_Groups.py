# 2._👥_Send_To_Contacts_Or_Groups.py is the page where the user can send messages to contacts or groups.
import subprocess
import streamlit as st
import os
from dotenv import load_dotenv

# get root path from .env file
load_dotenv()
root_path = os.getenv("root_path")

# large text area for the message
st.write("### Enter your message here:")


# button to open xlsx file with phone numbers
if st.button(rf'Open xlsx file with contacts\groups names'):
    subprocess.Popen(['start', rf'{root_path}\auto_whatsapper\data\contacts.xlsx'], shell=True)

if st.button('Open txt message'):
    subprocess.Popen(['start', rf'{root_path}\auto_whatsapper\data\message.txt'], shell=True)
#message = st.text_area(label=" ", height=300)
    
strip_and_try = st.checkbox('Strip contact names if not found, and try again', value=False)

if st.button('Send'):
    activate_script = os.path.join(root_path, 'wa', 'Scripts', 'activate.bat')
    script_path = os.path.join(root_path, 'auto_whatsapper', 'send_msgs.py')

    cmd = rf'pushd "{root_path}\auto_whatsapper" && call "{activate_script}" && start python "{script_path}" "contacts" "{strip_and_try}" && popd'
    subprocess.run(cmd, shell=True)
    st.write("Message sent!")