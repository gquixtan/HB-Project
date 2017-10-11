import json
import os
import requests

# gets API key
giphy_key = os.environ["GIPHY_API_KEY"]

# key word to query for giphys
# key_word = "hapy birthday"

# def get_giphy_key():
#     """ """ 
#     return giphy_key


def generates_json_giphys(key_word):
    """ generates """

    payload = {
            "q": key_word,
            "apikey": giphy_key,
                }

    r = requests.get("http://api.giphy.com/v1/gifs/search?", params=payload)
    response = r.json()

    return response


def create_embed_list(giphy_data):
    """ Loops through the data list that gets returned from the giphy api """

    # data hold a list of dictionaries with giphys
    data = giphy_data['data']

    # init an empty list that will be populated by all the return emb_urls from the giphy api
    giphy_list = []

    for obj in data:
        giphy_list.append(obj['embed_url'])
    return giphy_list

# data = generates_json_giphys(key_word)
# print generates_json_giphys(key_word)
# print
# print create_embed_list(data)
