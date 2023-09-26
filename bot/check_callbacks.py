

def check_callbacks(json_data):
    """
        ловим все коллбеки с клавиатур,
        достать дату из коллбека и подложить в ['message']['text']
    """

    if 'callback_query' in json_data:
        json_data['message'] = {}
        json_data['message']['chat'] = {}
        json_data['message']['chat']['id'] = json_data['callback_query']['from']['id']
        json_data['message']['chat']['username'] = None

        try:
            json_data['message']['chat']['username'] = json_data['callback_query']['from']['username']
        except KeyError:
            json_data['message']['chat']['username'] = None
        json_data['message']['text'] = json_data['callback_query']['data']
    
    else:
        try:
            json_data['message']['chat']['username'] = json_data['message']['chat']['username']
        except KeyError:
            json_data['message']['chat']['username'] = None
    
    return json_data