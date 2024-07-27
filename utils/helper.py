import spacy

import fitz
from spacy.lang.en import English


def format_text(text: str) -> str:
    """

    :param text:
    :return:
    """
    clean = text.replace("\n", " ").strip()
    print(clean)
    return clean


def get_text(file) -> dict:
    file.seek(0)
    doc = fitz.open(stream=file.read(), filetype='pdf')
    for pg in doc:
        print(f"_____{pg.number}_____ \n\n")
        text = format_text(pg.get_text())
        # text = text.split("\n\n") # get paragraphs
        pagewise_text = {"doc": file.name,
                         "page_num": pg.number,
                         "text": text
                         }
    return pagewise_text


def get_doc_sentences(doc_text_dict: dict) -> dict:
    """
    Return dictionary with text split into individual sentences

    :param doc_text_dict:
    :return:
    """
    nlp = English()
    nlp.add_pipe('sentencizer')

    for docname, page_text_dict in doc_text_dict.items():
        page_text_dict['sentences'] = list(str(nlp(page_text_dict['text']).sents))
        # page_text_dict['sentences'] = [str(sentence) for sentence in page_text_dict['sentences']]
        doc_text_dict[docname] = page_text_dict

    return doc_text_dict
