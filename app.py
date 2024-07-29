import streamlit as st
import time

from utils.prompts import PROMPT
from utils.helper import *


def main():
    st.set_page_config(layout="wide", page_title="Chat with PDF", page_icon=":robot_face:")
    ss = st.session_state

    # sidebar
    with st.sidebar:
        st.markdown("""
        # Chat with PDF :book:
        
        A RAG based document Q&A app. Upload your document and ask away!
        
        Code: [Github](https://github.com/adityapaikrao/document_qna) 
        """)
        # st.write("#### Upload your PDF to begin")
        files = st.file_uploader("Upload your PDF", type='pdf', accept_multiple_files=True)

        button_confirm = st.button('Confirm', key='confirm_upload')
        expander_config = st.expander('Configuration (Optional)', expanded=False if button_confirm else True)

        with expander_config:
            # models
            models = ["test", "test2"]
            st.selectbox("model", options=models, key="model")

            # prompts
            st.text_area("prompt", value=PROMPT["p1"], key='prompt')
            reset_db = st.radio('Reset DB?', options=['No', 'Yes'], index=0)

        if button_confirm and files:
            # with st.spinner(f"Processing {len(files)} document(s)..."):
            # start = time.time()
            doc_text = {}
            total_pages = 0
            for file in files:
                pdf_text = get_text(file)
                doc_text[file.name] = pdf_text
                total_pages += pdf_text[0]['num_of_pages']

            progress_bar = st.progress(0, 'Setting up...')
            # Process text & chunk together
            for docname, pagetext_list in doc_text.items():
                print(f'PREPARING {docname}....\n')
                pg_count = 0
                for text_dict in pagetext_list:
                    pg_count += 1
                    pg_num = text_dict['page_num']
                    progress_bar.progress(float(pg_count / total_pages),
                                          text=f'Processing {docname} Page {pg_num}')
                    print(f'PROCESSING PAGE NO', pg_num)
                    text_dict['sentences'] = get_sentences(text_dict['text'])
                    print('CHUNKING SOURCE PDF....')
                    text_dict['chunked_sentences'] = chunk_sentences(text_dict['sentences'])
                    print('EMBEDDING CHUNKED SENTENCES....\n')
                    text_dict['chunked_embeddings'] = get_chunked_embeddings(text_dict['chunked_sentences'])
                progress_bar.progress(100, 'Processed Successfully!')

            print('STORING TO YOUR DB...')

            # insert to DB
            store_to_db(doc_text, reset_db)


    # Main Window
    st.write('Ask a question!')


if __name__ == "__main__":
    main()
    print()
