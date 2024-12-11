
from streamlit.components.v1 import html


def jump_to_tab(tab_number: int):
    html(f"""
        <script>
            var tabGroup = window.parent.document.getElementsByClassName("stTabs")[0]
            var tab = tabGroup.getElementsByTagName("button")
            tab[{tab_number}].click()
        </script>
    """, height=0)
