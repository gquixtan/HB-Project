""" coonects to texts db """
from model import connect_to_db, db, User, Text
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from flask import Flask
import time
from datetime import datetime, date, timedelta
import pytz
import twilio_text


# create a function that does the query from db looking for send_out_date
# if there is one today or before today that needs to go out
# looop thro the things that need to go out from db 



def todays_query():
	""" Does a query for texts that need to be send out. """ 


	# print "*************************************"

	today = datetime.now()
	print "Today is ", today

	yesterday = today - timedelta(1)
	print "Yesterday is ", yesterday


	tomorrow = today + timedelta(1)
	print "Tomorrow is ", tomorrow


	
	todays_date = today.isoformat()
	today = todays_date[0:10]


	yesterdays_date = yesterday.isoformat()
	yesterday = yesterdays_date[0:10]

	tomorrows_date = tomorrow.isoformat()
	tomorrow = tomorrows_date[0:10]

	# doing a query for texts that need to be send out
	text = db.session.query(Text).filter((Text.send_out_date > yesterday ) & (Text.send_out_date < tomorrow)).all()

	print "text is ", text
	# print "*********************************"

	text_data = [ ]

	for item in text:
		print item
		text_data.append({"id": item.text_id, "keyword": item.keyword, "phone": item.phone, "msg": item.msg, "date": item.send_out_date, "sent": item.sent})

	return text_data


def new_func(text_data):
	""" """ 
	# print "this is the length of the list is: ", len(text_data)
	# print "*********************************"

	for item in text_data:
		keyword = item["keyword"]
		text_id = item["id"]
		# this is for twilio/giphy set up
		response = twilio_text.send_text(keyword)
		# print response

		sent = db.session.query(Text).filter(Text.text_id == text_id).first()
		# print sent


		if response.status == "queued":
			sent.sent=True
			db.session.add(sent)
			db.session.commit()
		else:
			sent.sent=False
			db.session.add(sent)
			db.session.commit()	


if __name__ == "__main__":
	# need this here to connect to db otherwise otherwise: "RuntimeError: No application found" 
    from server import app
    app = Flask(__name__)
    connect_to_db(app)

    todays_query()

    text_data = todays_query()
    new_func(text_data)

    # test = new_func(text_data)
    # sent(test)

