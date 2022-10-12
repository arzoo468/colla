import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
	return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
	TWILIO_ACCOUNT_SID = 'ACa3d6fad8e58e22fb9e39026a71424eb6'
	TWILIO_SYNC_SERVICE_SID = 'IS4e57cb1035645b9b82489fd6d5c8f53c'
	TWILIO_API_KEY = 'SKb240931f7e9a22a2106d7c26e7c9b8d7'
	TWILIO_API_SECRET = 'r038FuV8mojnA6O4bsceXNJSIwyCZ21P'

	username = request.args.get('username', fake.user_name())

	# create access token with credentials
	token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
	# create a Sync grant and add to token
	sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
	token.add_grant(sync_grant_access)
	return jsonify(identity=username, token=token.to_jwt().decode())

# A function to download text and store it in text file
@app.route('/', methods=['POST'])
def download_text():
	text_from_notepad = request.form['text']
	with open('workfile.txt', 'w') as f:
		f.write(text_from_notepad)

	path_to_store_txt = "workfile.txt"

	return send_file(path_to_store_txt, as_attachment=True)


if __name__ == "__main__":
	app.run(host='localhost', port='5001', debug=True)
