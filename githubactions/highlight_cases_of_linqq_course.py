

import urllib.parse

import requests

import json

import spacy

import os

import unicodedata
import re

"""# Helper Functions"""

def get_json_response (url):
  lingq_api_key = os.environ.get('LINGQ_API_KEY')
  if not lingq_api_key:
    raise ValueError("LINGQ_API_KEY is not set in the environment variables.")  
  headers = {
    'Authorization': f'Token {lingq_api_key}',
    'Content-Type': 'application/json'
  }
  response = requests.get(f'{url}?page_size=1000', headers=headers)
  return response.json()

def print_json (json_parsed):
  print (json.dumps(json_parsed, indent = 4))

def legal_filename(filename):
    # Convert to ASCII, removing non-ASCII characters
    filename = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode()
    
    # Replace remaining illegal characters with an underscore
    filename = re.sub(r'[^\w\-\. ]', '_', filename)
    
    # Remove leading and trailing whitespace, periods, and underscores
    filename = filename.strip(' ._')
    
    return filename


#@title Choose a language model
model = "pl_core_news_lg" #@param ["fi_core_news_lg", "de_core_news_lg", "en_core_web_lg", "nl_core_news_lg", "sv_core_news_lg", "da_core_news_lg", "pl_core_news_lg", "ru_core_news_lg", "uk_core_news_lg"]

nlp = spacy.load(model)

# Function to process text and return HTML with color-coded cases and tooltips
def process_and_display_paragraph(paragraph):
    doc = nlp(paragraph)
    highlighted_text = ""
    for token in doc:

      if token.pos_ == "PUNCT" :
        highlighted_text += token.text
      else :
        if not highlighted_text == "":
          highlighted_text += ' '
        # Retrieve morphological information
        case = token.morph.get("Case")
        morph = " ".join(f'{token.morph}'.split("|"))
        # Define the tooltip text
        tooltip_text = f"{token.lemma_} {token.pos_} ({morph})"
        morph_features = f'{token.morph}'.split("|")
        morph_features = [morph_feature.replace("=", "_") for morph_feature in morph_features]
        morph_features.append(token.pos_)
        styling_class = " ".join(morph_features)

        # Append the token span with style and tooltip
        highlighted_text += f'<span class="{styling_class}" data-tooltip="{tooltip_text}">{token.text}</span>'

    return f"<p>{highlighted_text}</p>"


course = get_json_response(f'https://www.lingq.com/api/v2/pl/collections/289027')
html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{course['title']}</title>
    <link rel="stylesheet" href="pl_case_styles.css">
    <script src="popup.js"></script>
</head>
<body>
"""

html += """

<p>Material is from <a href="https://www.lingq.com/">LingQ</a>, a language learning platform. This page was generated using a Python script that uses the LingQ API to fetch the course material and the spaCy library to process and display the text.</p>
<p>Key:</p>
<ul><li>Number
    <ul>
        <li class="Number_Plur">Plur</li>
        <li class="Number_Ptan">Ptan</li>
    </ul></li>
    <li>Gender
        <ul><li class="Gender_Masc">Masc</li>
        <li class="Gender_Fem">Fem</li>
        <li class="Gender_Neut">Neut</li>
        </ul></li>
    <li>Case
        <ul>
        <li class="Case_Nom">Nom</li>
        <li class="Case_Acc">Acc</li>
        <li class="Case_Ins">Ins</li>
        <li class="Case_Gen">Gen</li>
        <li class="Case_Loc">Loc</li>
        <li class="Case_Dat">Dat</li>
    </ul></li>
    <li>Animacy
        <ul>
        <li class="Animacy_Inan">Inan</li>
        <li class="Animacy_Nhum">Nhum</li>
        <li class="Animacy_Hum">Hum</li>
    </ul></li>
</ul>
<p>Hover your cursor over any word to see more morphological information, including what is the dictionary (lemmatized) form of the word and what part of speech it is in the context.</p>
"""

for lesson in course['lessons']:
  lesson_details = get_json_response(lesson['url'])
  paragraphs = get_json_response(lesson['url'] + 'paragraphs/')
  html += f"<h2>{lesson_details['title']}</h2>"
  for paragraph in paragraphs:
    joined_sentences = ' '.join(sentence['cleanText'] for sentence in paragraph['sentences'])
    html += process_and_display_paragraph(joined_sentences)

html += "</body></html>"

subfolder = "html_output/pl"
os.makedirs(subfolder, exist_ok=True)
html_file = os.path.join(subfolder, legal_filename(course['title']) + ".html")
with open(html_file, "w", encoding="utf-8") as file:
    file.write(html)

