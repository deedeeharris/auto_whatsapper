import streamlit as st

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