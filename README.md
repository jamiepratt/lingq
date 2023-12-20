#  [spaCy](https://spacy.io/) NLP for SRS

Some scripts to apply spaCy natural language processing to target language content to help adult foreign language learners get to grips with their target languages' grammar.

The idea is to take content that a learner is already familiar with and analyse the grammatical features of this content with spaCy.

We will take spaCy's output and produce a csv file that can be imported into a SRS such as Anki so that the learner can for example then expose themselves to categories of grammar such as:

* lots of examples of uses of a particular base form of a verb, noun, adjective etc with different cases, tenses, genders, in singular or plural etc. etc.
* OR examples of masculine plural nouns, in whatever case.
* examples of verbs in the third person, plural vs singular inflection.
* etc. etc.

By mining familiar content and categorising sentences according to their grammatical features we allow the learner to expose themselves to lots of examples of the grammatical feature they are interested in, in a progressive systematic way according to their whim, which we feel will help them to become familiar with the grammar patterns of their target language in as efficient a way as possible.

## Tools

### Done

#### [Export all your content from lingq into  a tree of text files in Google drive.](lingq_export.ipynb)

Discussed here: https://forum.lingq.com/t/export-your-lingq-text-content-as-a-tree-of-files-to-google-drive/164914

#### [Experiment to allow a user to select a single lesson from their lingq and run the content through spacy](lingq.ipynb)

Discussed here: https://forum.lingq.com/t/google-colab-notebook-to-select-a-language-course-lesson-and-then-to-run-natural-language-processing-from-spacy-on-the-text/164334

#### See also:

[This web app I created that allows you to enter text, select a Polish or English language model and enter some content to run through spaCY.](https://spacy-pl.streamlit.app/)
Remarkably simple code here: https://github.com/jamiepratt/spacy-pl/
### To do

#### Run text through spacy and produce a csv file

* iterates through a tree of text files on Google drive
* runs each text file through [spaCy.](https://spacy.io/)
* creates a db with records for every word in your content with linguistic features of that word such as:
  * the sentence the word appears in for context.
  * the base form of the word be it a verb, adjective or noun.
  * details of how the word is inflected eg. for verbs what person, tense, etc the verb is in or for Slavic nouns what case, etc the nouns are.