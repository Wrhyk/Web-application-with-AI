import requests, os, uuid, json
from flask import Flask, redirect, url_for, request, render_template, session
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def index_post():
    # Reading the values from the form
    original_text = request.form["text"]
    target_language = request.form["language"]

    # Loading the values from env
    key = os.environ["KEY"]
    endpoint = os.environ["ENDPOINT"]
    location = os.environ["LOCATION"]

    # Indicating that we want to translate and the api version and the target language
    path = '/translate?api-version=3.0'
    # Adding the target language parameter
    target_language_parameter = "&to=" + target_language
    # Creating the full url
    constructed_url = endpoint + path + target_language_parameter

    # Setting up header information
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Creating the body of the request with the text to be translated
    body = [{ "text": original_text }]

    # Making the call using POST
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    # Retriving the JSON response
    translator_response = translator_request.json()
    # Retriving the translation
    print(translator_response)
    translated_text = translator_response[0]["translations"][0]["text"]
    # Calling render template, passing on the translated text, original text, target language and template
    return render_template(
        "results.html",
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )