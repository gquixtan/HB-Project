from twilio.rest import Client
import os, giphy
import json
from random import choice, sample

my_number = os.environ["MY_NUMBER"]
twilio_number = os.environ["TWILIO_NUMBER"]
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]

def generates_giphy(lst):
    """ generates a giphy randomly from a list then uses giphy to be the body of the text """

    giphy_url = choice(lst)

    # print giphy_url
    return giphy_url    


def send_text(key_word):
    """sends a giphy using twilio api """

    # print key_word
    client = Client(account_sid, auth_token)

    data = giphy.generates_json_giphys(key_word)
    # print "I am data from the twilio file ", data

    giphy_list = giphy.create_embed_list(data)
    #  print giphy_list

    # this is the url that gets genarated by keyword in the db 
    url = generates_giphy(giphy_list)

    # calls the function below passing the keyword url 
    return send_text_url(url)

    # message = client.messages.create(
    #      to=my_number,
    #      from_=twilio_number,
    #      body=url)

    # return(message)

def send_text_url(url):
    """ sends a text pasing a url"""
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=my_number,
        from_=twilio_number,
        body=url)

    return(message)
