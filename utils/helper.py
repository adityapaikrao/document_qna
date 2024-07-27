from typing import List, Dict, Union

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


def get_text(file: object) -> dict:
    file.seek(0)
    doc = fitz.open(stream=file.read(), filetype='pdf')
    page_text = []
    for pg in doc:
        print(f"_____{pg.number}_____ \n\n")
        text = format_text(pg.get_text())
        # text = text.split("\n\n") # get paragraphs
        pagewise_text = {"doc": file.name,
                         "page_num": pg.number,
                         "text": text
                         }
        page_text.append(pagewise_text)
    return page_text


def get_sentences(text: str) -> List[str]:
    """
    Return list with text split into individual sentences

    :param text:
    :return:
    """
    nlp = English()
    nlp.add_pipe('sentencizer')

    sentences = [str(sentence) for sentence in nlp(text).sents]

    return sentences


def combine_sentences(sentences: list[str], buffer_size: int) -> list[dict[str, Union[str, int]]]:
    sentences = [{'sentence': x, 'index': i} for i, x in enumerate(sentences)]

    for i in range(len(sentences)):

        # Create a string that will hold the sentences which are joined
        combined_sentence = ''

        # Add sentences before the current one, based on the buffer size.
        for j in range(i - buffer_size, i):
            # Check if the index j is not negative (to avoid index out of range like on the first one)
            if j >= 0:
                # Add the sentence at index j to the combined_sentence string
                combined_sentence += sentences[j]['sentence'] + ' '

        # Add the current sentence
        combined_sentence += sentences[i]['sentence']

        # Add sentences after the current one, based on the buffer size
        for j in range(i + 1, i + 1 + buffer_size):
            # Check if the index j is within the range of the sentences list
            if j < len(sentences):
                # Add the sentence at index j to the combined_sentence string
                combined_sentence += ' ' + sentences[j]['sentence']

        # Then add the whole thing to your dict
        # Store the combined sentence in the current sentence dict
        sentences[i]['combined_sentence'] = combined_sentence

    return sentences


def chunk_sentences(doc_text_sentences: List[str], buffer_size: int = 1) -> None:
    """

    :param doc_text_sentences:
    :param buffer_size:
    :return:
    """
    combined_sentences = combine_sentences(doc_text_sentences, buffer_size)
    print()
