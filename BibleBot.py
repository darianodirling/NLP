import os
import streamlit as st

# Streamlit setup
st.subheader("Bible Bot")

# Using provided API key and project ID
api_key = "sn9zkSxyWwc6Kb5Tz1wV4wziOrZv-1sQNjAYL8TtSfWZ"
project_id = "d5737ca5-0ca5-4b92-a391-a2a0281154bf"


# Function to get IBM Watson credentials
def get_credentials():
    return {
        "url" : "https://us-south.ml.cloud.ibm.com",
        "apikey" : api_key
    }

# Model setup
model_id = "meta-llama/llama-2-70b-chat"

parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 100,
    "stop_sequences": ["\n\n"],
    "repetition_penalty": 1
}

space_id = os.getenv("SPACE_ID")

from ibm_watson_machine_learning.foundation_models import Model

# Function to create the chatbot model
def make_model(model_id, parameters, project_id, space_id):
    model = Model(
        model_id = model_id,
        params = parameters,
        credentials = get_credentials(),
        project_id = project_id,
        space_id = space_id
        )

    return model

# Prompt input containing questions and answers
prompt_input = """
You're building a Biblical Wisdom Chatbot to provide guidance and advice rooted in scripture. 
Your task is to create a chatbot that responds to user inquiries with relevant biblical quotes and advice. 
Your bot should be able to handle various types of questions related to life, faith, morality, and more. 
The goal is to create a conversational experience where users can seek wisdom and guidance from the Bible.

Your prompt should generate responses that:

1. Understand the user's query and context.
2. Retrieve relevant biblical quotes or advice based on the query.
3. Present the retrieved information in a coherent and helpful manner.

Your task is to write code that achieves this functionality. You may use any programming language and libraries of your choice. 
Ensure that your chatbot provides accurate and meaningful responses consistent with biblical teachings. 
Test your chatbot with different queries to ensure its effectiveness and accuracy.

Question: What does the Bible say about forgiveness?
Answer: "Forgive us our debts, as we also have forgiven our debtors." - Matthew 6:12

Question: How can I find peace in troubled times?
Answer: "Peace I leave with you; my peace I give you. Do not let your hearts be troubled and do not be afraid." - John 14:27

Question: What does the Bible say about love?
Answer: "Love is patient, love is kind. It does not envy, it does not boast, it is not proud." - 1 Corinthians 13:4

Question: How can I overcome temptation?
Answer: "Submit yourselves, then, to God. Resist the devil, and he will flee from you." - James 4:7

Question: What is the purpose of life according to the Bible?
Answer: "For we are God’s handiwork, created in Christ Jesus to do good works." - Ephesians 2:10

Question: How should I treat others?
Answer: "Do to others as you would have them do to you." - Luke 6:31

Question: How can I have faith during difficult times?
Answer: "Trust in the Lord with all your heart and lean not on your own understanding." - Proverbs 3:5
"""

# Attempt to create the chatbot model
try:
    model = make_model(model_id, parameters, project_id, space_id)
except Exception as e:
    st.text("Waiting for keys")

# Streamlit UI for interaction with the bot
try:
    st.title('Ask the NLP Bot')

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])

    prompt = st.text_input('Ask your question here')

    if prompt:
        st.chat_message('user').markdown(prompt)

        st.session_state.messages.append({'role': 'user', 'content': prompt})

        LLM_Response = model.generate_text(prompt=prompt_input + prompt + "Answer: ")

        st.chat_message('assistant').markdown(LLM_Response)

        st.session_state.messages.append({
            'role': 'assistant', 'content': LLM_Response
        })
except Exception as e:
    st.text("Correct keys have not been entered yet")
