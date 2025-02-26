# Loading Necessary Dependencies
import streamlit as st

from langchain_community.document_loaders import YoutubeLoader
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_ollama import ChatOllama

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

    def summarize_video(self, url: str):
        '''
        This method will take url and summarize it and returns it
        '''

        try:
            # Intializing LLM
            llm = ChatOllama(model = 'gemma:2b')

            # Creating our prompt template
            template = """
            Summarize the following video transcript:
            {text}
            """

            # Creating our prompt
            prompt = PromptTemplate(template=template, input_variables=["text"])

            # Creating our chain
            chain = load_summarize_chain(
                llm = llm,
                chain_type = 'stuff',
                prompt = prompt,
            )

            # Loading our documents
            documents = self.load_url(url=url)

            # Invoking our chain
            response = chain.invoke(documents)

            return response
        
        except Exception as e:
            print(e)

# Creating our Streamlit app
st.title('Youtube Video Summarizer')
st.write('summarize youtube video with llm')

url = st.text_input('Enter Youtube URL...')

if st.button('Summarize Video'):
    youtube_summarizer = YoutubeSummarizer()
    response = youtube_summarizer.summarize_video(url=url)

    if response:
        st.success(response)

    else:
        st.warning('Error Occured While Summarizing Video')