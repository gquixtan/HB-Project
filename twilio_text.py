from twilio.rest import Client
import os, giphy
import urllib
import json
from random import choice, sample

my_number = os.environ["MY_NUMBER"]
twilio_number = os.environ["TWILIO_NUMBER"]
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]


def generates_giphy(lst):
    """ generates a giphy from random to text """

    giphy_url = choice(lst)
    return giphy_url


def send_text(key_word):
    """ """
    client = Client(account_sid, auth_token)

    data = giphy.generates_json_giphys(key_word)

    giphy_list = giphy.create_embed_list(data)

    message = client.messages.create(
        to=my_number,
        from_=twilio_number,
        body=generates_giphy(giphy_list))

    return(message.sid)

send_text("happy")