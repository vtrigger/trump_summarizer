import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

def add_bg_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.7)), 
                             url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'result' not in st.session_state:
    st.session_state.result = None

st.set_page_config(layout="wide")

# Add the background image
add_bg_image("https://static.politico.com/c2/74/d1467d224ed888f7b6b2b4d8c599/160816-donald-trump-getty-1160.jpg")

st.markdown(
    """
    <h1 style='
        text-align: center; 
        color: #ff6b00; 
        font-family: "Comic Sans MS", cursive;
        font-size: 3rem;
        -webkit-text-stroke: 1px black;
        text-stroke: 1px black;
        margin-top: -50px !important;
        margin-bottom: 30px;
    '>TRUMSPLAINING</h1>
    """, 
    unsafe_allow_html=True
)

prompt = PromptTemplate(
    template="""Give a summary of the article provided below as if you are Donald Trump
    article: {article}""",
    input_variables=['article']
)

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

parser = StrOutputParser()

chain = prompt | llm | parser

# Only show input if not processed yet
if not st.session_state.processed:
    article_link = st.text_input("Paste article URL here: ")
    
    if article_link:
        try:
            with st.spinner("Trumpsplaining the article... (this might take a moment)"):
                docs = WebBaseLoader(web_path=article_link).load()
                result = chain.invoke({'article': docs[0].page_content})
                
                st.session_state.result = result
                st.session_state.processed = True
                
                st.rerun()
                
        except Exception as e:
            st.error(f"Error processing article: {e}")

else:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(
        f"""
        <div style='
            background-color: rgba(255, 255, 255, 0.95);
            padding: 25px;
            border-radius: 15px;
            border: 2px solid #ff6b00;
        '>
        <p style='
            font-size: 16px;
            line-height: 1.6;
            color: #333;
            font-weight: 500;
        '>{st.session_state.result}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    if st.button("🔄 Analyze Another Article"):
        st.session_state.processed = False
        st.session_state.result = None
        st.rerun()
