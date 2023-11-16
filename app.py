## importing streamlit
import streamlit as st
## Loading .env file and api keys
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)


#### Steps:-
## 1. importing chat models from openai
## 2. Adding the memory to the custom_chatgpt app, so that we can chat and ask folow up question of the previous one
## 3. Adding chat history in the app

from langchain.chat_models import ChatOpenAI
from langchain.schema import(
    AIMessage, SystemMessage, HumanMessage
)
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

## imports for memory
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory, FileChatMessageHistory

## ------------------------------------------------------------------------------------------------------
def ask_chatBot(content):
    myllm = ChatOpenAI(model_name = 'gpt-3.5-turbo', temperature = 1)

    ## chat history storing
    myChatHistory = FileChatMessageHistory('chat_history.json')

    ## memory for the chatmodel
    mymemory = ConversationBufferMemory(
        memory_key = 'chat_history',
        chat_memory = myChatHistory,
        return_messages= True
    )

    myprompt = ChatPromptTemplate(
        input_variables=["content"],
        messages = [
            SystemMessage(content="you are a chatbot having a conversation with a human"),
            MessagesPlaceholder(variable_name = 'chat_history'), ## This is where the memory will be stored and it should be placed after SystemMessage and before HumanMessagePromptTemplate
            HumanMessagePromptTemplate.from_template('{content}')
        ]
    )

    chain = LLMChain(
        llm = myllm,
        prompt = myprompt,
        ##adding memory
        memory = mymemory,
        verbose=False)
    
    myresponse = chain.run({'content': content})
    return myresponse
#     #### ------ Creating infinite while loop not to end the conversation between the chatbot and the user -------

# while True:
#         content = input("PLease ask your query: ")
#         loopBreakList = ['quit', 'close', 'exit', 'bye']
#         ## If user enters any word word which matches with the loopBreakLst list, caht will be stooped
#         if content in loopBreakList:
#             print('Goodbye, have a great day!')
#             break
#         ## Else chat will return the response from the LLm, and it will continue
#         else:
#             response = chain.run({'content': content})
#             print(response)
#             print('*' * 50)


## Initializing streamlit app
st.set_page_config(page_title="Custom Chatbot")
st.header("Langchain Chatbot Application")
## Taking the input from user
input = st.text_input("Input: ", key="input")
response = ask_chatBot(input)

submit = st.button("Ask your queston")

## If ask button is clicke
if submit:
    st.subheader("The Response is: ")
    st.write(response)

###### For running the code -------> streamlit run app.py