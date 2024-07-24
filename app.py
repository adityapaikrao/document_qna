import streamlit as st
from utils.prompts import PROMPT


def main():
    st.set_page_config(layout="wide", page_title="Chat with PDF", page_icon=":robot_face:")

    # add details on the sidebar
    with st.sidebar:
        st.markdown("""
        # Chat with PDF 
        
        A document Q&A interface. Upload your PDF and ask away!
        
        source code: [Github](https://github.com/adityapaikrao/document_qna) 
        """)
        st.write("")
        with st.expander("Advanced Configuration"):
            # models
            models = ["test", "test2"]
            st.selectbox("model", options=models, key="model")

            #prompts
            st.text_area("prompt", value=PROMPT["p1"], key='prompt')


if __name__ == "__main__":
    main()
