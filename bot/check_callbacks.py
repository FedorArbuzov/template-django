

def check_callbacks(json_data):
    """
        ловим все коллбеки с клавиатур,
        достать дату из коллбека и подложить в ['message']['text']
    """

    if 'callback_query' in json_data:
        json_data['message'] = {}
        json_data['message']['chat'] = {}
        json_data['message']['chat']['id'] = json_data['callback_query']['from']['id']
        json_data['message']['text'] = json_data['callback_query']['data']
    
    return json_data