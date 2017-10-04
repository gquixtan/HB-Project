""" coonects to texts db """
from model import connect_to_db, db, User, Text
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from flask import Flask
import time
from datetime import datetime, date, timedelta
import pytz


# create a function that does the query from db looking for send_out_date
# if there is one today or before today that needs to go out
# looop thro the things that need to go out from db 


def todays_query():
	""" search for texts """ 

	pacific = pytz.timezone('US/Pacific')

	today = datetime.now(tz=pacific)
	# print "today is ", today
	yesterday = today - timedelta(1)

	print "yesterday is ", yesterday

	todays_date = today.isoformat()
	today = todays_date[0:10]


	yesterdays_date = yesterday.isoformat()
	yesterday = yesterdays_date[0:10]

	# doing a query for texts that need to be send out
	text = db.session.query(Text).filter((Text.send_out_date == today) | (Text.send_out_date == yesterday)).all()
	print "*********************************"
	print "text is ", text
	print "*********************************"

	text_data = []

	for item in text:
		text_data.append(item.keyword)
		text_data.append(item.phone)
		text_data.append(item.send_out_date)


	return text_data

if __name__ == "__main__":
	# need this here to connect to db otherwise otherwise: "RuntimeError: No application found" 
    from server import app
    app = Flask(__name__)
    connect_to_db(app)
    print todays_query()	

