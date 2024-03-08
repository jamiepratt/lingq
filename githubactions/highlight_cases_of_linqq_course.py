

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
        tooltip_text = f"{token.lemma_} {token.pos_}"
        if morph:
            tooltip_text += f"<br> ({morph})"
        morph_features = f'{token.morph}'.split("|")
        morph_features = [morph_feature.replace("=", "_") for morph_feature in morph_features]
        morph_features.append(token.pos_)
        styling_class = " ".join(morph_features)

        # Append the token span with style and tooltip
        highlighted_text += f'<span class="{styling_class}" data-tooltip="{tooltip_text}">{token.text}</span>'

    return f"<p>{highlighted_text}</p>"


js = """
    document.addEventListener('DOMContentLoaded', function() {
        // Function to create the popup
        function createPopup(text, target) {
            const popup = document.createElement('div');
            popup.classList.add('popup');
            popup.innerHTML = text;
            document.body.appendChild(popup);

            // Position the popup above the target element
            const rect = target.getBoundingClientRect();

            // Adjust the position to account for scrolling
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
            popup.style.left = `${rect.left}px`;
            popup.style.top = `${rect.bottom + scrollTop - popup.offsetHeight + 5}px`;
            popup.style.display = 'block';
        }

        // Function to remove the popup
        function removePopup() {
            const popup = document.querySelector('.popup');
            if (popup) {
                popup.remove();
            }
        }

        // Attach event listeners to elements with data-tooltip
        const elements = document.querySelectorAll('[data-tooltip]');
        elements.forEach(el => {
            el.addEventListener('mouseenter', function() {
                const tooltipText = this.getAttribute('data-tooltip');
                createPopup(tooltipText, this);
            });

            el.addEventListener('mouseleave', function() {
                removePopup();
            });
        });
    });
"""

course = get_json_response(f'https://www.lingq.com/api/v2/pl/collections/1646225')
html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{course['title']}</title>
    <link rel="stylesheet" href="pl_case_styles.css">
    <script>
    {js}
    </script>
</head>
<body>
"""

html += """
<div class="preamble">
<p>Material is from <a href="https://www.lingq.com/">LingQ</a>, a language learning platform. This page was generated using a Python script that uses the LingQ API to fetch the course material and the spaCy library to process and display the text.</p>
<p>Key:</p>
<ul><li>Number
    <ul>
        <li><span class="Number_Plur">Plur</span></li>
        <li><span class="Number_Ptan">Ptan</span></li>
    </ul></li>
    <li>Gender
        <ul><li><span class="Gender_Masc">Masc</span></li>
        <li><span class="Gender_Fem">Fem</span></li>
        <li><span class="Gender_Neut">Neut</span></li>
        </ul></li>
    <li>Case
        <ul>
        <li><span class="Case_Nom">Nom</span></li>
        <li><span class="Case_Acc">Acc</span></li>
        <li><span class="Case_Ins">Ins</span></li>
        <li><span class="Case_Gen">Gen</span></li>
        <li><span class="Case_Loc">Loc</span></li>
        <li><span class="Case_Dat">Dat</span></li>
    </ul></li>
    <li>Animacy
        <ul>
        <li><span class="Animacy_Inan">Inan</span></li>
        <li><span class="Animacy_Nhum">Nhum</span></li>
        <li><span class="Animacy_Hum">Hum</span></li>
    </ul></li>
</ul>
<p>Hover your cursor over any word to see more morphological information, including what is the dictionary (lemmatized) form of the word and what part of speech it is in the context.</p>
</div>
"""

for lesson in course['lessons']:
  paragraphs = get_json_response(lesson['url'] + 'paragraphs/')
  html += "<div class='lesson'>"
  html += f"<h2>{lesson['title']}</h2>"
  for paragraph in paragraphs:
    joined_sentences = ' '.join(sentence['cleanText'] for sentence in paragraph['sentences'])
    html += process_and_display_paragraph(joined_sentences)
  html += "</div>"

html += "</body></html>"

subfolder = "html_output/pl"
os.makedirs(subfolder, exist_ok=True)
html_file = os.path.join(subfolder, legal_filename(course['title']) + ".html")
with open(html_file, "w", encoding="utf-8") as file:
    file.write(html)

