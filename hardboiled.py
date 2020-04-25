from flask import Flask, render_template, request
from myapp.forms import QuerySearchForm

app = Flask(__name__)

import re

import numpy as np
import pandas as pd
import nltk

pd.set_option('display.max_colwidth', -1)

nltk.download('stopwords')

from nltk.corpus import stopwords
from scipy.spatial.distance import cosine

# Load embeddings
GLOVE_FILE = 'glove.6B.300d.txt'
EMBEDDINGS = {}
print('Loading embeddings')
with open(GLOVE_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        EMBEDDINGS[word] = coefs
print('Done!')

# Other parameters
STOP_WORDS = set(stopwords.words('english'))
LETTERS_RE = re.compile('[^a-z ]+')
DEFAULT_CHOICES = ['Come again?', 'What did you say?', 'I am sorry, I did not get that']
THRESHOLD = 0.5


def get_sentence_vector(sentence):
    vecs = [EMBEDDINGS.get(word) for word in sentence.split() if word in EMBEDDINGS]
    return np.mean(vecs, axis=0)


def similarity(str1, str2):
    vec1 = get_sentence_vector(str1)
    vec2 = get_sentence_vector(str2)
    return 1 - cosine(vec1, vec2)


def query(user_input, options):
    scores = pd.DataFrame([], columns=['option', 'score'])
    for option in options:
        scores = scores.append(
            pd.DataFrame([[option, sum([similarity(word, option) for word in user_input if word not in STOP_WORDS])]],
                         columns=['option', 'score']),
            ignore_index=True
        )
    return scores.sort_values('score', ascending=False)


def fast_search(user_input):
    with open('options', 'r') as f:
        options = [line.strip() for line in f.readlines()]
    return query(user_input, options)


@app.route('/', methods=['GET', 'POST'])
def index():
    search = QuerySearchForm(request.form)
    user_input = LETTERS_RE.sub('', search.data['search'].lower()).split()
    if request.method == 'POST':
        options_scores = fast_search(user_input)
        return render_template('index.html', form=search, results=True,
                               tables=options_scores.to_html(classes='results', header="true"))
    return render_template('index.html', form=search, results=False, tables=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
