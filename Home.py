import streamlit as st
from typing import Optional
from page.scan_page import ScanPage
from page.scan_progress_view import ScanProgressView
from page.Mask import MaskPage
from protectoMethods import ProtectoAPI
from page.masking_configuration_page import MaskConfigPage
from page.login_page import LoginPage
from page.masking_approval_page import MaskingApprovalPage 
from page.mask_progress import MaskProgressPage

VALID_PAGES = {"home", "scan_edit", "scan_progress", "mask", "mask_config", "mask_approval", "mask_progress"}

import streamlit as st
from typing import Optional

import streamlit as st
from typing import Optional

import streamlit as st
from typing import Optional

import streamlit as st
from typing import Optional

import streamlit as st
from typing import Optional

import streamlit as st
from typing import Optional

import streamlit as st
from typing import Optional

class ImprovedSidebar:
    
    def __init__(self):
        self.css = """
            <style>
            .stApp {background-color: white;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            section[data-testid="stSidebar"] {
                background-color: #1e3d59;
                padding: 2rem 1rem;
            }
            
            /* Direct targeting of radio button text */
            section[data-testid="stSidebar"] .st-emotion-cache-eczf16 {
                color: white !important;
                font-size: 1.5rem !important;
                font-weight: 500 !important;
            }

            /* Target the radio input */
            section[data-testid="stSidebar"] input[type="radio"] {
                width: 24px !important;
                height: 24px !important;
                border: 2px solid white !important;
                margin-right: 12px !important;
            }

            /* Additional radio text targeting */
            section[data-testid="stSidebar"] div.st-emotion-cache-ocqkz7 {
                color: white !important;
            }

            section[data-testid="stSidebar"] div.st-emotion-cache-ocqkz7 p {
                color: white !important;
                font-size: 1.5rem !important;
            }

            /* Radio container */
            section[data-testid="stSidebar"] .st-emotion-cache-1inwz65 {
                margin: 1.5rem 0;
            }

            /* Dropdown styling */
            section[data-testid="stSidebar"] .stSelectbox select {
                background-color: white;
                color: black !important;
            }

            section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
                background-color: white !important;
                border-radius: 4px !important;
            }

            section[data-testid="stSidebar"] .stSelectbox [data-testid="stMarkdown"] p {
                color: black !important;
                font-size: 1.2rem !important;
            }

            section[data-testid="stSidebar"] div[role="listbox"] {
                background-color: white !important;
                border-radius: 4px !important;
            }

            section[data-testid="stSidebar"] div[role="option"] {
                color: black !important;
                background-color: white !important;
                padding: 0.75rem !important;
            }

            section[data-testid="stSidebar"] hr {
                margin: 2rem 0;
                border-color: #ffffff40;
            }

            /* Force white color on all radio text */
            section[data-testid="stSidebar"] [role="radiogroup"] * {
                color: white !important;
            }
            </style>
        """

    def show_sidebar(self):
        st.markdown(self.css, unsafe_allow_html=True)
        
        with st.sidebar:
            st.markdown("""
    <h1 style="color: white; font-weight: bold; letter-spacing: 2px; font-family: Arial, sans-serif; font-size: 17px;">P R O T E C T O</h1>
    """, unsafe_allow_html=True)            
            if st.button("Change Environment", use_container_width=True):
                for key in list(st.session_state.keys()):
                    if key != 'selected_object':
                        del st.session_state[key]
                st.session_state.authenticated = False
                st.session_state.page = 'login'
                st.rerun()
            
            st.markdown("<hr/>", unsafe_allow_html=True)
            
            # Radio buttons with explicit styling
            st.markdown(
                """
                <style>
                .st-emotion-cache-1inwz65 p {
                    color: white !important;
                    font-size: 1.5rem !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            
            main_nav = st.radio(
                "Navigation",
                options=["Scan", "Mask"],
                label_visibility="collapsed"
            )
            
            if main_nav == "Scan":
                scan_option = st.selectbox(
                    "",
                    options=["Start Scan", "Scan Progress"],
                    key="scan_submenu"
                )
                
                if scan_option == "Start Scan":
                    st.session_state.page = "scan_edit"
                elif scan_option == "Scan Progress":
                    st.session_state.page = "scan_progress"
            
            elif main_nav == "Mask":
                mask_option = st.selectbox(
                    "",
                    options=[
                        "Mask Configuration",
                        "Mask Approval",
                        "Mask Progress"
                    ],
                    key="mask_submenu"
                )
                
                if mask_option == "Mask Configuration":
                    st.session_state.page = "mask_config"
                elif mask_option == "Mask Approval":
                    st.session_state.page = "mask_approval"
                elif mask_option == "Mask Progress":
                    st.session_state.page = "mask_progress"

class ProtectoApp:
    def __init__(self):
        self._configure_page()
        self._init_session_state()
        self.protecto_api = ProtectoAPI()
        self.scan_page = ScanPage()
        self.scan_progress = ScanProgressView(self.protecto_api)
        self.sidebar = ImprovedSidebar()

    def _configure_page(self) -> None:
        st.set_page_config(page_title="Protecto Vault", layout="wide")

    def _init_session_state(self) -> None:
        if 'page' not in st.session_state:
            st.session_state.page = "home"

    def home(self) -> None:
        st.markdown("""<div style="margin-top: 20%;"></div>""", unsafe_allow_html=True)
        st.markdown(
            """<p style='text-align: center; color: grey; font-size: 1.5em; margin-bottom: 0;'>
            Make Your Enterprise Data</p>""", 
            unsafe_allow_html=True
        )
        st.markdown("""<div class="protecto-vault">Protecto Vault</div>""", unsafe_allow_html=True)
        st.markdown(
            """<h3 style='text-align: center; color: grey; font-size: 2.5em;'>
            Secure approach to data security and privacy</h3>""", 
            unsafe_allow_html=True
        )
        st.markdown(
            """<p style='text-align: center; color: black; font-size: 1.0em; margin-bottom: 65px;'>
            Protecto identifies and masks sensitive data while maintaining context and semantic meaning, 
            ensuring accuracy in your LLMs/Gen AI apps.</p>""", 
            unsafe_allow_html=True
        )

    def render_page(self) -> None:
        try:
            if st.session_state.authenticated:
                if st.session_state.page == "home":
                    self.home()
                elif st.session_state.page == "scan_edit":
                    self.scan_page.show_start_scan()
                elif st.session_state.page == "scan_progress":
                    self.scan_progress.render()
                elif st.session_state.page == "mask":
                    MaskPage().show()
                elif st.session_state.page == "mask_config":
                    MaskConfigPage().show()
                elif st.session_state.page == "mask_approval":
                    MaskingApprovalPage().show()   
                elif st.session_state.page == "mask_progress":
                    MaskProgressPage().show()     
        except Exception as e:
             st.error(f"Error rendering page: {str(e)}")

    def run(self) -> None:
        #st.session_state.authenticated=True
        try:
            # Initialize authentication state if not present
            if 'authenticated' not in st.session_state:
                st.session_state.authenticated = False
                st.session_state.page = 'login'
    
            # Show login page if not authenticated
            if not st.session_state.authenticated:
                login_page = LoginPage()
                login_page.display()
                return
            else:
                # Always set home page as default after login
                if st.session_state.page == 'login':
                    st.session_state.page = 'home'
    
            # Show sidebar and render page if authenticated
            self.sidebar.show_sidebar()
            self.render_page()
            
        except Exception as e:
            st.error(f"Error in application: {str(e)}")

if __name__ == "__main__":
    app = ProtectoApp()
    app.run()