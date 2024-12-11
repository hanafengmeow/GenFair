from typing import Any

import streamlit as st
from streamlit.components.v1 import html


def init_session_states(defaults: dict[str, Any]):
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
            

def jump_to_tab(tab_number: int):
    html(f"""
        <script>
            var tabGroup = window.parent.document.getElementsByClassName("stTabs")[0]
            var tab = tabGroup.getElementsByTagName("button")
            tab[{tab_number}].click()
        </script>
    """, height=0)
