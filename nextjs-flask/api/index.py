from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import asyncio
import os
import redis
import string
import time
from collections import defaultdict

import nltk
nltk.download('punkt')
nltk.download('words')
nltk.download('stopwords')
from nltk.metrics.distance import jaccard_distance
from nltk.util import ngrams

from nltk.corpus import words
from rake_nltk import Rake
from krovetzstemmer import Stemmer

correct_words = words.words()
rake_nltk_var = Rake()

ALPHABET = string.ascii_lowercase
STEMMER = Stemmer()

SEARCH_CUTOFF = 10

r = None

load_dotenv("..")
# app instance
app = Flask(__name__)
CORS(app)

def zero_list():
    return [0, 0]

def retrieve_word_info(word, words_info):
    word = STEMMER.stem(word)

    urls = list(r.smembers(f"word:{word}")) # Get urls for word
    word_dict = dict()
    print(len(urls))
    pipe = r.pipeline()
    for i in range(len(urls)): # Process metadata through pipeline
        urls[i] = urls[i].decode('utf-8')
        pipe.lrange(f"metadata:{word}:{urls[i]}", 0, -1)
    metadata_list = pipe.execute()
    for i in range(len(urls)):
        metadata = metadata_list[i]
        url = urls[i]
        metadata[0] = int(metadata[0].decode('utf-8')) 
        metadata[1] = float(metadata[1].decode('utf-8'))
        word_dict[url] = metadata
    words_info[word] = word_dict

def init_words_info(args, words_info):
    for word in args:
        retrieve_word_info(word, words_info)

def add_titles(relevant_urls):
    pipe = r.pipeline()
    for i in range(len(relevant_urls)):
        pipe.get(f"title:{relevant_urls[i]}")
    titles = pipe.execute()
    for i in range(len(relevant_urls)):
        relevant_urls[i] = (relevant_urls[i], titles[i].decode('utf-8'))

def and_query(urls_dict):
    intersection_set = set()
    initiated = False
    for key in urls_dict.keys():
        if not initiated:
            intersection_set = set(urls_dict[key].keys())
            initiated = True
        else:
            intersection_set = intersection_set.intersection(set(urls_dict[key].keys()))
    return intersection_set


def calc_url_scores(query_result, words_info):
    url_scores_dict = defaultdict(
        zero_list
    )  # default value is a list where important score is 0 and tfidf score is 0
    for word in words_info:
        for url in query_result:
            url_scores_dict[url][0] += words_info[word][url][0]
            url_scores_dict[url][1] += words_info[word][url][1]

    url_scores_list = list(
        sorted(
            url_scores_dict.keys(),
            key=lambda x: (-url_scores_dict[x][0], -url_scores_dict[x][1]),
        )
    )
    return url_scores_list


def calc_new_url_scores(url_scores_list, words_info):
    temp = calc_url_scores(and_query(words_info), words_info)
    for v in temp:
        if v not in url_scores_list:
            url_scores_list.append(v)
        if len(url_scores_list) >= SEARCH_CUTOFF:
            break

    return url_scores_list


def get_least_relevant_word(avg_dict):
    return list(avg_dict.keys())[list(avg_dict.values()).index(min(avg_dict.values()))]


def remove_least_relevant_words_info(words_info):
    avg_tfidfs = dict()
    for word, data in words_info.items():
        tfidfs = [tfidf for _, tfidf in data.values()]
        if len(tfidfs) > 0:
            avg_tfidfs[word] = sum(tfidfs) / len(tfidfs)

    least_relevant_word = get_least_relevant_word(avg_tfidfs)
    args = list(words_info.keys())
    args.remove(least_relevant_word)

    words_info = dict()
    init_words_info(args, words_info)
    return words_info


def autocorrect_words_info(words_info):
    keys = list(words_info.keys())
    args = list()

    for word in keys:
        temp = [
            (jaccard_distance(set(ngrams(word, 2)), set(ngrams(w, 2))), w)
            for w in correct_words
            if w[0] == word[0]
        ]
        args.append(sorted(temp, key=lambda val: val[0])[0][1])

    words_info = dict()
    init_words_info(args, words_info)
    return words_info


def get_keywords_words_info(words_info):
    keys = " ".join(list(words_info.keys()))

    rake_nltk_var.extract_keywords_from_text(keys)
    keyword_extracted = rake_nltk_var.get_ranked_phrases()
    args = [word for keyword in keyword_extracted for word in keyword.split()]
    
    words_info = dict()
    init_words_info(args, words_info)
    return words_info


def sort_relevant(words_info):  # sort relevance of url by highest tfidf score
    # FIRST screen
    print("1st screen: " + str(list(words_info.keys())))
    url_scores_list = calc_url_scores(and_query(words_info), words_info)

    # SECOND screen - extract keywords
    if len(url_scores_list) < SEARCH_CUTOFF:
        words_info = get_keywords_words_info(words_info)
        print("2nd screen: " + str(list(words_info.keys())))
        url_scores_list = calc_new_url_scores(url_scores_list, words_info)

    # THIRD screen - autocorrect words
    if len(url_scores_list) < SEARCH_CUTOFF:
        words_info = autocorrect_words_info(words_info)
        print("3rd screen: " + str(list(words_info.keys())))
        url_scores_list = calc_new_url_scores(url_scores_list, words_info)

    # FOURTH screen - remove least relevant tfidf score (often misinterpreted autocorrect)
    if len(url_scores_list) < SEARCH_CUTOFF and len(words_info) > 1:
        words_info = remove_least_relevant_words_info(words_info)
        print("4th screen: " + str(list(words_info.keys())))
        url_scores_list = calc_new_url_scores(url_scores_list, words_info)

    return url_scores_list

def search(args, host=None, port=None, password=None):
    for i in range(len(args)):  # lowercase all words
        args[i] = args[i].lower()

    global r
    r = redis.Redis(host=host, port=port, password=password)

    # FIRST SCREEN - remove single characters
    args = list(filter(lambda x: len(x) > 1, args))
    words_info = dict()
    start_time = time.time()
    init_words_info(args, words_info)
    print(f"It took {time.time() - start_time} seconds to run init words info")

    relevant_urls = sort_relevant(words_info)
    print(f"LENGTH OF RELEVANT URLS: {len(relevant_urls)}")
    start_time = time.time()
    add_titles(relevant_urls)
    print(f"It took {time.time() - start_time} seconds to add titles")

    for i, url in enumerate(relevant_urls[:SEARCH_CUTOFF]):
        print(f"{i + 1}: {url[0]}, {url[1]}")
    print(len(relevant_urls))
    return relevant_urls

@app.route("/api/search", methods=["GET"])
def return_home():
    query = request.args.getlist("query")
    query_params = query[0].split(" ")
    length = int(request.args.getlist("length")[0])
    result = search(query_params, host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"], password=os.environ["REDIS_PASS"])
    result_dict = dict()
    removed_links = 0
    for i in range(len(result)):
        if i - removed_links >= length:
            break
        url, title = result[i]
        result_dict[i - removed_links] = [url, title]
    return jsonify({
        "result" : result_dict
    })


if __name__ == "__main__":
    app.run()