# Loading Necessary Dependencies
import streamlit as st
import validators

from langchain_community.document_loaders import YoutubeLoader
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
# from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq

# Creating our main logic
class YoutubeSummarizer:
    def load_url(self, url: str):
        '''
        This method will load url and returns the url
        '''
        try:
            # Splitting Video id from url
            video_id = url.split('v=')[-1]

            # Loading our URL
            loader = YoutubeLoader(video_id, add_video_info=False)
            documents = loader.load()

            return documents 

        except Exception as e:
            print(e)
            st.error(e)

    def summarize_video(self, url: str, api_key: str):
        '''
        This method will take url and summarize it and returns it
        '''

        try:
            # Intializing LLM
            llm = ChatGroq(
                model = 'Gemma-7b-It',
                groq_api_key = api_key
            )

            # Creating our prompt template
            template = """
            Summarize the following video transcript in 300 words:
            {text}
            """

            # Creating our prompt
            prompt = PromptTemplate(template=template, input_variables=["text"])

            # Creating our chain
            chain = load_summarize_chain(
                llm = llm, 
                chain_type = 'stuff',
                prompt = prompt,
                verbose=True
            )

            # Loading our documents
            documents = self.load_url(url=url)

            # Invoking our chain
            response = chain.invoke(documents)

            return response
        
        except Exception as e:
            print(e)
            st.error(e)

# Creating our Streamlit app
st.title('Youtube Video Summarizer')
st.write('summarize youtube video with llm')

with st.sidebar:
    groq_api_key = st.text_input('Groq API Key', type='password', placeholder='Enter your Groq API Key')

if not groq_api_key:
    st.error('Please provide a API key for Groq LLM')

url = st.text_input('Enter Youtube URL...')

if not validators.url(url):
    st.error('Please provide a valid Youtube URL')

if st.button('Summarize Video'):
    youtube_summarizer = YoutubeSummarizer()
    response = youtube_summarizer.summarize_video(url=url, api_key=groq_api_key)

    if response:
        st.success(response)

    else:
        st.error('Error Occured While Summarizing Video')