from urllib.parse import urlparse
from bs4 import BeautifulSoup
import urllib
import requests

import re
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

from gensim import corpora
import gensim




### Get all URLs from a YouTube channel ###

def get_all_URLs(playlist_url):

    # playlist_url = 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV'
    page = requests.get(playlist_url)
    text = str(BeautifulSoup(page.content, 'html.parser'))
    URLs = []
    unique = '<td class="pl-video-title">'
    right = 0

    while True:
        start = text.find(unique, right)
        left = text.find('href="', start) + 6
        right = text.find('"', left)

        if left >= 6 and right > left:
            candidate = text[left:right]
            URLs.append('https://www.youtube.com' + candidate)
        else:
            break

    return URLs



### Get all videoIDs from URLs -extracted from a youtube channel ###

def get_videoIDs(URLs):
    video_IDs = []
    for url in URLs:
        url_data = urlparse(url)
        query = urllib.parse.parse_qs(url_data.query)
        video_IDs.append(query["v"][0])
    return video_IDs

### Implementing LDA(Latent Dirichlet Allocation) Model - Topic Modeling ###

def LDA(video_IDs, number_of_topics, number_of_words):
    doc_set = []

    # Import & clean my documents

    for ID in video_IDs:
        video_sub_url = 'http://video.google.com/timedtext?lang=en&v=' + ID
        page = requests.get(video_sub_url)
        soup = BeautifulSoup(page.content, "html.parser")
        doc = str(soup.get_text()).lower()
        doc = re.sub("[^-a-zA-Z]+", " ", doc)
        doc_set.append(doc)
    tokenizer = RegexpTokenizer(r'\w+')
    texts = []

    # Tokenization & stopwords & stemming

    for doc in doc_set:
        tokenizer.tokenize(doc)
        tokens = tokenizer.tokenize(doc)
        stop = set(stopwords.words('english'))
        stopped_tokens = [i for i in tokens if not i in stop and len(i)> 1]

        #p_stemmer = PorterStemmer
        #stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

        texts.append(stopped_tokens)
    # Constructing a document-term matrix
    dictionary = corpora.Dictionary(texts)
    doc_term_matrix = [dictionary.doc2bow(txt) for txt in texts]

    # Applying the LDA model

    lda = gensim.models.LdaModel
    ldamodel = lda(doc_term_matrix, num_topics = number_of_topics, id2word = dictionary, passes = 200)
    return ldamodel.print_topics(num_topics= number_of_topics, num_words= number_of_words)

