import subprocess
import streamlit as st
import os


root_path = rf'C:\ai\whatsapp'

# large text area for the message
st.write("### Enter your message here:")


# button to open xlsx file with phone numbers
if st.button('Open xlsx file with phone numbers'):
    subprocess.Popen(['start', rf'{root_path}\auto_whatsapper\data\numbers.xlsx'], shell=True)

message = st.text_area(label=" ", height=300)

if st.button('Send'):
    activate_script = os.path.join(root_path, 'wa', 'Scripts', 'activate.bat')
    script_path = os.path.join(root_path, 'auto_whatsapper', 'send_msgs.py')

    cmd = rf'pushd "{root_path}\auto_whatsapper" && call "{activate_script}" && start python "{script_path}" "numbers" "{message}" && popd'
    subprocess.run(cmd, shell=True)
    st.write("Message sent!")