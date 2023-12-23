import streamlit as st

if 'num_characters' not in st.session_state:
    st.session_state['num_characters'] = st.slider('Number of characters per exercise', 2, 12, 4)
else:
    st.session_state['num_characters'] = st.slider('Number of characters per exercise', 2, 12, st.session_state['num_characters'])
st.write("Current value ", st.session_state['num_characters'])