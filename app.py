import streamlit as st

from utils.chunker import get_text, get_sentences, chunk_sentences, get_embeddings
from utils.chroma import store_to_db, get_context_from_db
from utils.llm_chat import get_llm_response, response_generator


def main():
    global chat_history
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
            # models = ["test", "test2"]
            # st.selectbox("model", options=models, key="model")

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
                    text_dict['chunked_embeddings'] = get_embeddings(text_dict['chunked_sentences'])
                progress_bar.progress(100, 'Processed Successfully!')

            print('STORING TO YOUR DB...')

            # insert to DB
            store_to_db(doc_text, reset_db)

    # Main Window
    st.write('Ask a question!')

    if 'messages' not in ss:
        ss['messages'] = []

    for message in ss['messages']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Interface
    if query := st.chat_input("Got questions?"):
        # Add user message to chat history
        ss['messages'].append({"role": "user", "content": query})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(query)

        # get relevant context
        context = get_context_from_db(query)
        response_text = get_llm_response(query, ss['messages'], context=context)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            # st.markdown(response)
            response = st.write_stream(response_generator(response_text))
        # Add assistant response to chat history
        ss['messages'].append({"role": "assistant", "content": response})
    print()


if __name__ == "__main__":
    main()
    print()
