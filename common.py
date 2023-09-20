import streamlit as st


def set_header(header_name):
    st.markdown("""<p style="color:#00568D; padding:5px 15px; font-family:'Segoe UI'; font-size:20px;">
                        <b>""" + header_name + """</b></p>""", True)
