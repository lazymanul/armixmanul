# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="回念",
        page_icon="👋",
    )

    st.write("# Welcome to 回念 project 👋")

    #st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        This is a ML System Design 2023 course project by FractalCat and armixket  
        **👈 Use menu from the sidebar** to start exploration  
        
        * Hello page (you are here) 
        * Setup page. Select diffculty level
        * Practice game 1. A game where you should match spelling of the character to its image.
        
        
        """
    )
    st.image("pics/boy.jpg")


if __name__ == "__main__":
    run()
