import streamlit as st
from fpdf import FPDF
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

from fpdf import FPDF

def export_chat_to_pdf(chat_history):
    if chat_history:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        line_height = 10
        cell_width = 190  # Set the width of the cell for wrapping

        for index, message in enumerate(chat_history):
            # Alternating speaker assumption based on index
            speaker = "User" if index % 2 == 0 else "Bot"
            content = getattr(message, 'content', 'No Content')
            # Use multi_cell for automatic text wrapping within the specified width
            pdf.multi_cell(cell_width, line_height, txt=f"{speaker}: {content}", border=0)

        # Save the PDF to a temporary file
        pdf_output = "chat_history.pdf"
        pdf.output(pdf_output)
        return pdf_output
    else:
        return None

def handle_userinput(user_question):
    # Ensure that there is a conversation model initialized
    if 'conversation' in st.session_state and callable(st.session_state.conversation):
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history = response['chat_history']

        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
    else:
        st.error("The conversation model is not initialized. Please upload documents and process them to initialize the conversation model.")

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat With Projects", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.header("Chat with projects :books:")
    
    # Using form to clear input after submission
    with st.form("question_form", clear_on_submit=True):
        user_question = st.text_input("Ask a question about your documents:", key="query")
        submit_button = st.form_submit_button("Ask")
        if submit_button and user_question:
            handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            if pdf_docs:
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    if raw_text:
                        text_chunks = get_text_chunks(raw_text)
                        vectorstore = get_vectorstore(text_chunks)
                        if vectorstore:
                            st.session_state.conversation = get_conversation_chain(vectorstore)
                        else:
                            st.error("Failed to create a vector store from the text.")
                    else:
                        st.error("No text could be extracted from the uploaded PDFs.")
        if st.button("Clear Chat"):
            st.session_state.conversation = None
            st.session_state.chat_history = []
            st.experimental_rerun()
    
        # In the main function, within the Streamlit UI setup:
        if st.sidebar.button("Download Chat History as PDF"):
            pdf_file = export_chat_to_pdf(st.session_state.chat_history)
            if pdf_file:
                with open(pdf_file, "rb") as file:
                    btn = st.sidebar.download_button(
                        label="Download PDF",
                        data=file,
                        file_name="chat_history.pdf",
                        mime="application/octet-stream"
                    )

if __name__ == '__main__':
    main()

