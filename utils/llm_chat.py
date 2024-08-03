import time
import ollama
from utils.prompt import PROMPT, PROMPT_INITIAL



def response_generator(response):
    """

    :param response:
    :return:
    """
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


def get_llm_response(query, history, context, buffer_window=2, model='gemma2:2b'):
    """

    :param model:
    :param query:
    :param history:
    :param context:
    :param buffer_window:
    :return:
    """
    buffer_window = buffer_window*2 + 1

    if len(history) - buffer_window < 0:
        # include all history
        start_index = 0
    else:
        # determine start index and get windowed history
        start_index = len(history) - buffer_window

    params = {'query': query, 'context': context}

    if len(history) <= 1:
        params = {'query': query, 'context': context}
        prompt = PROMPT_INITIAL.format(**params)

    else:
        history_text = ''
        for idx in range(start_index, len(history)):
            content = history[idx]
            history_text += f"{content['role']}: {content['content']}\n"
        params['history'] = history_text
        prompt = PROMPT.format(**params)

    response = ollama.generate(model=model, prompt=prompt)

    return response['response']
