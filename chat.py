import streamlit as st
import random
import time
import requests
import json
import yaml

projects = []
project_ids = []


def load_config():
    with open('config.yaml', 'r') as file:
        config_content = yaml.safe_load(file)
    return config_content


config = load_config()
api_key = config['AAI-Brain']['API-KEY']
api_secret = config['AAI-Brain']['API-Secret']


def clear_session_state():
    st.session_state.messages = []
    print("cleared")


def create_chat(project_id):
    st.session_state.messages = []
    url_create = "https://api.getodin.ai/chat/create"
    payload = json.dumps({'project_id': project_id})
    headers = {
        "accept": "application/json",
        "X-API-KEY": api_key,
        "X-API-SECRET": api_secret,
        "content-type": "application/json"
    }
    response_create = requests.post(url_create, data=payload, headers=headers)
    conv_id = json.loads(response_create.content)["chat_id"]
    return conv_id


def get_projects():
    url_projects = "https://api.getodin.ai/projects"
    headers = {
        "accept": "application/json",
        "X-API-KEY": api_key,
        "X-API-SECRET": api_secret,
    }

    response_projects = requests.get(url_projects, headers=headers)
    projects_json = json.loads(response_projects.content)
    global projects
    projects = [project for project in projects_json['projects']]
    global project_ids
    project_ids = [project['name'] for project in projects_json['projects']]
    return projects, project_ids


# Call Projects function to fill the select-box element
get_projects()


@st.experimental_fragment
def sidebar_update():
    project_name = st.selectbox(
        "Select Project name",
        project_ids,
        index=None,
        placeholder="Select Project name...",
    )

    for project in projects:
        if project['name'] == project_name:
            project_id_selected = project['id']
            st.session_state["project_id_selected"] = project_id_selected



# Create streaming Object from Response
def response_generator(response_str):
    full_response = ""
    for word in response_str:
        time.sleep(0.01)
        yield word

st.set_page_config(page_title='El Salvador - Automation Anywhere - AAI Brain', page_icon = 'https://chat-beta.automationanywhere.com/assets/icon/favicon.ico', layout='wide')
st.header("San Salvador - Automation Anywhere - AAI Brain")
# st.image("https://chat-beta.automationanywhere.com/static/media/aa-gen-ai-logo.17572d7b831dd1a39cf8.png")
st.html("""
    <!doctype html>
    <html lang="en">
    <head>
    	<meta charset="utf-8"/>
    <title>AAI Enterprise Knowledge</title>
    </head>
    <body>
    <center> 
    <img src=https://chat-beta.automationanywhere.com/static/media/aa-gen-ai-logo.17572d7b831dd1a39cf8.png width=200>
    <br>
    <img src=data:image/jpeg;base64,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 width=250>
    </center>
    </html>
""")

# Create a sidebar using Streamlit's built-in function
with st.sidebar:
    # Call the sidebar_update() function decorator
    sidebar_update()
    # Create a primary button in the sidebar with the label "Create a new Chat"
    if st.button("Create a new Chat", type="primary"):
        clear_session_state()
        clear_session_state()
        # Set the value of the session state variable 'chat_id' to the result of calling create_chat()
        # with the 'project_id_selected' value from the session state
        st.session_state['chat_id'] = create_chat(st.session_state["project_id_selected"])


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get('image', 0) != 0:
            # print(message["image"])
            st.image(message["image"], 'Generated Image(s)')
        else:
            st.markdown(message["content"])
            # pass


# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    session_state_test = st.session_state
    # Check if a chat ID has been set in the session state.
    # If not, check if a project ID has been selected.
    if session_state_test.get('chat_id', 0) == 0:
        # If no chat ID, but a project ID has been selected, create a new chat.
        if session_state_test.get('project_id_selected', 0) == 0:
            # Display a toast message prompting the user to select a project.
            st.toast('Select a project first', icon='🚨')
            st.stop()
        else:
            # Create a new chat with the selected project ID and set it as the chat ID.
            st.session_state["chat_id"] = create_chat(st.session_state['project_id_selected'])

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display user message in chat message container
    with st.chat_message("assistant"):
        chat_id = st.session_state["chat_id"]
        project_id = st.session_state["project_id_selected"]
        print(f"chat with project {project_id}")
        url_message = "https://api.getodin.ai/v2/chat/message"
        payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"agent_type\"\r\n\r\nchat_agent\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{chat_id}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"message\"\r\n\r\n{prompt}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"project_id\"\r\n\r\n{project_id}\r\n-----011000010111000001101001--"
        chat_headers = {
            "accept": "application/json",
            "X-API-KEY": api_key,
            "X-API-SECRET": api_secret,
            "content-type": "multipart/form-data; boundary=---011000010111000001101001"
        }

        response = requests.post(url_message, data=payload, headers=chat_headers)

        response_message = st.write_stream(response_generator(json.loads(response.text)['message']['response']))
        images = []
        if (json.loads(response.text)['message']).get('image_urls', 0) != 0:
            print('got an image')
            print(json.loads(response.text)['message']['image_urls'][0])

            for index, image in enumerate(json.loads(response.text)['message']['image_urls'], start=1):
                images.append(image)
            image_message = st.image(images, caption=f'Generated Image(s)')
    if len(images) > 0:
        st.session_state.messages.append({"role": "assistant", "content": response_message})
        st.session_state.messages.append({"role": "assistant", "image": images})
    else:
        st.session_state.messages.append({"role": "assistant", "content": response_message})


