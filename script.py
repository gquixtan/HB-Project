""" coonects to texts db this script should be ran everyday at 1pm (PT)"""
from model import connect_to_db, db, User, Text
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from flask import Flask
import time
from datetime import datetime, date, timedelta
import twilio_text


# todays_query does the query from the db:
# if there is one today or before today that needs to go out

def todays_query():
	""" Does a query for texts that need to be send out. """ 

	# today is based on UTC (7 hours ahead of actual time)
	today = datetime.now()
	print "Today is ", today
	print "*********************************"

	# yesterday is set to UTC time (1 day behind)
	yesterday = today - timedelta(days=2)
	print "Yesterday is ", yesterday
	print "*********************************"	


	# tomorrow is set to UTC time (1 day ahead)
	tomorrow = today + timedelta(days=1)
	print "Tomorrow is ", tomorrow
	print "*********************************"
	
	todays_date = today.isoformat()
	today = todays_date[0:10]


	yesterdays_date = yesterday.isoformat()
	yesterday = yesterdays_date[0:10]

	tomorrows_date = tomorrow.isoformat()
	tomorrow = tomorrows_date[0:10]

	# doing a query for texts that need to be send out (UTC time is 7 hours ahead of Pacific Time)
	text = db.session.query(Text).filter((Text.send_out_date > yesterday ) & (Text.send_out_date < tomorrow) & (Text.sent == "f")).all()

	print "text is ", text
	print "*********************************"

	# for t in text:
	# 	if t.keyword is not None:
	# 		print t.keyword, t.send_out_date, t.sent

	# print text.filter_by(Text.keyword).all


	print "------------------------------------"



	# crerating a list of nested dicts and each dict is a text,
	text_data = [ ]

	for item in text:
		# print item
		# creating a dict and adding it to text_data list
		text_data.append({"id": item.text_id, "keyword": item.keyword, "phone": item.phone, "url": item.url,  "date": item.send_out_date, "sent": item.sent})

	print "I am the list of nested dictionaries: ", text_data
	# "url": item.url,
	print "--------------------"


	return text_data


def send_text(text_data):
	""" This function is passing a nested list of dicts & checks for texts that need to be send and if they alredy were sent for the day
	they do not get resend """

	# print "INSID THE SEND_TEXT: ", text_data


	for item in text_data:
		keyword = item["keyword"]
		text_id = item["id"]
		# url = item["url"]
		status = item["sent"]

		print "I am a keyword in send text func ", keyword

		

		# This checks for text status and if it was succefully sent it will not send it again. 
		if status == True:
			return "*** ALREADY SENT ***"

		# if keyword is not empty send the text	
		# elif keyword != '' and keyword is not None: 
	elif keyword:
		
			# this is for twilio/giphy response
			# print 'keyword', keyword
			# raise

			response = twilio_text.send_text(keyword)

			# response2 = twilio_text.send_text_url(url)

			# this checks status of the sent text and updates the DB.
			sent = db.session.query(Text).filter(Text.text_id == text_id).first()

			# if the response of a text is succesful then the status of sent becomes True.
			if response.status == "queued":
				sent.sent=True
				db.session.add(sent)
				db.session.commit()

		print "*** successfully sent & added to db ***"	


if __name__ == "__main__":
	# need this here to connect to db otherwise otherwise: "RuntimeError: No application found" 
    from server import app
    app = Flask(__name__)
    connect_to_db(app)

    todays_query()

    text_data = todays_query()
    print send_text(text_data)

