import random as ra
import openai as ai
import os
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = os.urandom(42)

SYLLABLES = [
    "a",   "e",   "i",   "o",   "u",
   "ja",  "je",  "jo",  "ju",  "ka",
   "ke",  "ki",  "ko",  "ku",  "la",
   "le",  "li",  "lo",  "lu",  "ma",
   "me",  "mi",  "mo",  "mu",  "na",
   "ne",  "ni", "nja", "nje", "njo",
  "nju", "nka", "nke", "nki", "nko",
  "nku", "nla", "nle", "nli", "nlo",
  "nlu",  "no", "npa", "npe", "npi",
  "npo", "npu", "nsa", "nse", "nsi",
  "nso", "nsu", "nta", "nte", "nto",
  "ntu",  "nu", "nwa", "nwe", "nwi",
   "pa",  "pe",  "pi",  "po",  "pu",
   "sa",  "se",  "si",  "so",  "su",
   "ta",  "te",  "to",  "tu",  "wa",
   "we",  "wi",
];

class KeyForm(FlaskForm):
    key = PasswordField('OpenAI key', validators=[DataRequired()])
    submit = SubmitField('o mama e nimisin')

@app.route('/', methods=['GET', 'POST'])
def index():
    # starting content
    nimisin = "ilo samu"
    definition = "o mama e nimisin kepeken pali lili"
    field_visibility = "visible"
    field_position = "relative"

    # submitted content
    form = KeyForm()
    if form.validate_on_submit():
        flash('key submitted...')
        key = form.key.data
        ai.api_key = key

        # build nimisin from syllables
        ra.seed()
        ch_a = ra.choice(SYLLABLES)
        if ch_a[0] == "n" and len(ch_a) == 3:
            ch_a = ch_a[1:3]
        ch_b = ra.choice(SYLLABLES)
        nimisin = ch_a + ch_b

        for _ in range(0,ra.randint(0,3)):
            ch_c = ra.choice(SYLLABLES)
            nimisin += ch_c

        # ai query for definition
        prompt = "define this fictional toki pona word in 5 words: \"" + nimisin + "\"\n"
        ai_query = ai.Completion.create(
            engine="text-davinci-002",
            prompt= prompt,
            max_tokens=75,
            temperature=0.7,
            top_p=1,
        )   
        definition = ai_query["choices"][0]["text"][1:].lower()

        field_visibility = "hidden"
        field_position = "absolute"

    return render_template('index.html', form=form, nimisin=nimisin, \
                           definition=definition, field_visibility=field_visibility, \
                           field_position=field_position)

if __name__ == '__main__':
    app.run()
