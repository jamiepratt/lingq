

import urllib.parse

import requests

import json

import spacy

import os

import unicodedata
import re

print(f"requests=={requests.__version__}")
print(f"spacy=={spacy.__version__}")

"""# Helper Functions"""

def get_json_response (url):
  lingq_api_key = os.environ.get('LINGQ_API_KEY')
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
        highlighted_text += f'<span class="{styling_class}" title="{tooltip_text}">{token.text}</span>'

    return f"<p>{highlighted_text}</p>"

css_style = """
<style>
    .Gender_Fem::after {
        content: " ♀";
        color: pink;
        background-color:white;
    }
    .Gender_Masc::after {
        content: " ♂";
        color: blue;
        background-color:white;
    }
    .Gender_Neut::after {
      content: " ⚧";
      color: black;
      background-color:white;

    }
    .Gender_Neut:hover,
    .Gender_Masc:hover,
    .Gender_Fem:hover {border: 1px dashed black;}

    .Number_Ptan, .Number_Plur {
    text-decoration: underline;
    text-decoration-color: currentColor;
    }
    .Number_Ptan {
      text-decoration-style: dashed;

    }

    .Case_Ins {
        color: orange;
    }
    .Case_Acc {color:green;}

.Case_Nom {color: yellow; background-color:lightgray}

.Case_Gen {color: burlywood}

.Case_Loc {color:white; background-color:lightgray }

.Case_Dat {color:aqua; background-color:lightgray }
</style>


"""

course = get_json_response(f'https://www.lingq.com/api/v2/pl/collections/289027')

html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{course['title']}</title>
    <style>
{css_style}
    </style>
</head>
<body>
"""

html += """
<p>Key:</p>
<ul>
<li class="Number_Plur">Number_Plur</li>
<li class="Number_Ptan">Number_Ptan</li>
<li class="Gender_Masc">Gender_Masc</li>
<li class="Gender_Fem">Gender_Fem</li>
<li class="Gender_Neut">Gender_Neut</li>
<li class="Case_Nom">Case_Nom</li>
<li class="Case_Acc">Case_Acc</li>
<li class="Case_Ins">Case_Ins</li>
<li class="Case_Gen">Case_Gen</li>
<li class="Case_Loc">Case_Loc</li>
<li class="Case_Dat">Case_Dat</li>
</ul>
"""

for lesson in course['lessons']:
  lesson_details = get_json_response(lesson['url'])
  paragraphs = get_json_response(lesson['url'] + 'paragraphs/')
  html += f"<h2>{lesson_details['title']}</h2>"
  for paragraph in paragraphs:
    joined_sentences = ' '.join(sentence['cleanText'] for sentence in paragraph['sentences'])
    html += process_and_display_paragraph(joined_sentences)

html += "</body>"

subfolder = "html_output"
os.makedirs(subfolder, exist_ok=True)
html_file = os.path.join(subfolder, legal_filename(course['title']) + ".html")
with open(html_file, "w", encoding="utf-8") as file:
    file.write(html)
    print("HTML output written to output.html")

