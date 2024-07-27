import streamlit as st

from utils.prompts import PROMPT
from utils.helper import *


def main():
    st.set_page_config(layout="wide", page_title="Chat with PDF", page_icon=":robot_face:")

    # sidebar
    with st.sidebar:
        st.markdown("""
        # Chat with PDF :book:
        
        A RAG based document Q&A app. Upload your document and ask away!
        
        Code: [Github](https://github.com/adityapaikrao/document_qna) 
        """)
        st.write("")
        with st.expander("Advanced Configuration"):
            # models
            models = ["test", "test2"]
            st.selectbox("model", options=models, key="model")

            # prompts
            st.text_area("prompt", value=PROMPT["p1"], key='prompt')

    # main window
    st.write("# Upload your PDFs below:")
    files = st.file_uploader("", type='pdf', accept_multiple_files=True)
    if st.button("Confirm") and files:
        with st.spinner("Processing..."):
            doc_text = {}
            for file in files:
                pdf_text = get_text(file)
                doc_text[file.name] = pdf_text

            # Process text & chunk together
            for docname, pagetext_list in doc_text.items():
                for text_dict in pagetext_list:
                    text_dict['sentences'] = get_sentences(text_dict['text'])
                    text_dict['chunked_sentences'] = chunk_sentences(text_dict['sentences'])
                    text_dict['']




            st.write("Files Processed Successfully...!")


if __name__ == "__main__":
    main()
    print()
