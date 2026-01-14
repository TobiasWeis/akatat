import binascii
import requests
from flask import render_template, Blueprint, jsonify, request, abort

from const_transliteration import tandaschwili_gippert_transliteration
from flaskdb import db
from models import Customer, Translation, TranslationSource

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
		translated_words[-1]["transliterated"] = transliterate_(word)

		for translation_source in db.session.query(TranslationSource).all():
			# first, check if the word is in the database already
			translation = db.session.query(Translation).filter_by(word=word).first()

			translated_words[-1]["source_name"] = translation_source.source_name

			if translation is None:
				query_string = ""

				if translation_source.query_format == "georgian_bytes":
					a = binascii.hexlify(word.encode('utf8'))
					b = bytes([int(a[i:i + 2], 16) for i in range(0, len(a), 2)])

					for b_ in b:
						query_string += f"%{b_:x}"

					print(f"----Query string: {query_string.upper()}---")

				r = requests.get(translation_source.source_url.replace("%s", query_string.upper()))

				try:
					translated_words[-1]["out"] = r.json()['found'][0]['en']
				except Exception as e:
					print(e)
					translated_words[-1]["out"] = f"???"

				# save to database to save time next query
				translation = Translation(
					word=word,
					translation=translated_words[-1]["out"],
					id_source=translation_source.id)
				db.session.add(translation)
				db.session.commit()
			else:
				translated_words[-1]["out"] = translation.translation

	return jsonify({'translation': translated_words})

def transliterate_(input_text):
	out = ''
	for letter in input_text:
		if letter == ' ':
			out += ' '
			continue
		if letter not in tandaschwili_gippert_transliteration:
			out += letter
		else:
			out += tandaschwili_gippert_transliteration[letter]
	return out

@app_blueprint.route('/transliterate/', methods=['POST'])
def transliterate():
	input_text = request.json['input_text']
	out = transliterate_(input_text)
	return jsonify({"transliterated": out})
