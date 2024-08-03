import chromadb
from utils.chunker import get_embeddings


def store_to_db(doc_text, reset_db):
    """

    :param doc_text:
    :param reset_db:
    :return:
    """
    client = chromadb.PersistentClient(path='./db')
    if reset_db == 'Yes':
        try:
            client.delete_collection('vector_store')
            print('Deleted')
        except:
            print('Could Not Delete collection..')
    collection = client.get_or_create_collection(name='vector_store')

    for docname, pagewise_data in doc_text.items():
        for page_data in pagewise_data:
            for i, embeddings in enumerate(page_data['chunked_embeddings']):
                page_num = page_data['page_num']
                if i % 50 == 0:
                    client.heartbeat()
                collection.add(documents=page_data['chunked_sentences'][i],
                               metadatas=[{'docname': docname, 'page_num': page_num}],
                               ids=[f'{docname}-{page_num}-{i}'],
                               embeddings=[embeddings]
                               )
    print('Vectorized DB succesfully..')


def get_context_from_db(query):
    """

    :param query:
    :param collectionname:
    :return:
    """
    embeddings = get_embeddings([query])

    client = chromadb.PersistentClient(path='./db')
    collection = client.get_or_create_collection(name='vector_store')
    context = collection.query(query_embeddings=embeddings, n_results=3)

    docs = context['documents'][0]
    return '\n'.join(docs[0])
