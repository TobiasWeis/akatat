import binascii
import requests
from flask import render_template, Blueprint, jsonify, request, abort

from const_transliteration import tandaschwili_gippert_transliteration
from flaskdb import db
from models import Customer


app_blueprint = Blueprint('app',__name__)

@app_blueprint.route('/')
@app_blueprint.route('/app')
def index():
	return render_template("index.html")

@app_blueprint.route('/customer')
def return_customers():
	customers = db.session.query(Customer).all()

	return jsonify([customer.to_dict() for customer in customers])

@app_blueprint.route('/translate/', methods=['POST'])
def translate():
	input_text = request.json['input_text']

	translated_words = []

	for word in input_text.split():
		translated_words.append({'in': word})
		a = binascii.hexlify(word.encode('utf8'))
		b = bytes([int(a[i:i + 2], 16) for i in range(0, len(a), 2)])

		query_string = ""
		for b_ in b:
			query_string += f"%{b_:x}"

		translated_words[-1]["transliterated"] = transliterate_(word)

		print(f"----Query string: {query_string.upper()}---")

		r = requests.get(f"https://beta2.translate.ge/api/translate?from=ka&to=en&str={query_string.upper()}")
		try:
			translated_words[-1]["out"] = r.json()['found'][0]['en']
		except Exception as e:
			print(e)
			translated_words[-1]["out"] = f"???"

	return jsonify({'translation': translated_words})

def transliterate_(input_text):
	out = ''
	for letter in input_text:
		if letter == ' ':
			out += ' '
			continue
		if letter not in tandaschwili_gippert_transliteration:
			out += '-'
		else:
			out += tandaschwili_gippert_transliteration[letter]
	return out

@app_blueprint.route('/transliterate/', methods=['POST'])
def transliterate():
	input_text = request.json['input_text']
	out = transliterate_(input_text)
	return jsonify({"transliterated": out})
