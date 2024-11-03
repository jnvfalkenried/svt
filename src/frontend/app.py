import os
import streamlit as st
import streamlit_authenticator as stauth
from pyngrok import ngrok
from dotenv import load_dotenv
import logging
import yaml
from yaml.loader import SafeLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_ngrok():
    load_dotenv()  # Load environment variables from .env file
    NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")

    if NGROK_AUTH_TOKEN is None:
        logger.warning("Ngrok Auth Token is not set.")
        return None
    else:
        try:
            ngrok.set_auth_token(NGROK_AUTH_TOKEN)
            tunnels = ngrok.get_tunnels()
            if tunnels:
                public_url = tunnels[0].public_url  # Use the first active tunnel
                logger.info(f"App is publicly available at: {public_url}")
                return public_url
            else:
                public_url = ngrok.connect(8501)
                logger.info(f"App is publicly available at: {public_url}")
                return public_url
        except Exception as e:
            logger.error(f"Failed to set up Ngrok: {e}")
            return None

def login():
    with open('./config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Pre-hashing all plain text passwords once
    stauth.Hasher.hash_passwords(config['credentials'])

    with open('./config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    if st.session_state['authentication_status']:
        st.sidebar.success("You are logged in! Select a page above.")

        st.write(f"# Welcome {st.session_state['name']} to the TikTok Fake News Detector")
        st.write("""
            Welcome to the **TikTok Fake News Detector** application. This tool is designed to help users identify and analyze 
            the credibility of news content shared on TikTok. With the rise of misinformation on social media platforms, this 
            app aims to provide a solution for fact-checking and determining the authenticity of information.
        """)
        st.write("### Key Features")
        st.write("""
        - **Statistics**: View insightful statistics on detected fake news trends.
        - **Search**: Use keywords or upload images to search for content authenticity.
        - **About**: Learn more about this application and the technology behind it.
        """)
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] is None:
        try:
            authenticator.login()
        except Exception as e:
            st.error(e)
        st.warning('Please enter your username and password')

def logout():
    with open('./config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Pre-hashing all plain text passwords once
    stauth.Hasher.hash_passwords(config['credentials'])

    with open('./config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    st.write(f"# Goodbye {st.session_state['name']}")
    authenticator.logout()
    

def main():
    st.set_page_config(
        page_title="TikTok Fake News Detector",
        page_icon=":material/newspaper:",
    )
    # Set up Ngrok only if it hasn't been set up before
    if 'ngrok_url' not in st.session_state:
        public_url = setup_ngrok()
        if public_url:
            st.session_state.ngrok_url = public_url

    if "authentication_status" not in st.session_state:
        st.session_state.authentication_status = None

    login_page = st.Page(login, title="Log in", icon=":material/login:")
    logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

    dashboard = st.Page("pages/trends.py", title="TikTok Trends", icon=":material/dashboard:")
    alerts = st.Page("pages/alerts.py", title="Alerts", icon=":material/notification_important:")

    search = st.Page("pages/search.py", title="Multimodal Search", icon=":material/search:")
    # history = st.Page("tools/history.py", title="History", icon=":material/history:")

    bugs = st.Page("pages/bugs.py", title="Bug reports", icon=":material/bug_report:")
    about = st.Page("pages/about.py", title="About", icon=":material/info:")


    if st.session_state.authentication_status:
        pg = st.navigation(
            {
                "Account": [logout_page],
                "Reports": [dashboard, alerts],
                "Tools": [search],
                "Help": [bugs, about],
            }
        )
    else:
        pg = st.navigation([login_page])

    pg.run()

if __name__ == "__main__":
    main()
