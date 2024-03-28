from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import redis.asyncio as redis
import asyncio
import os
import string
import time
import math
import functools
from collections import defaultdict

import nltk
nltk.download('punkt', download_dir="/tmp/nltk_data")
nltk.download('words', download_dir="/tmp/nltk_data")
nltk.download('stopwords', download_dir="/tmp/nltk_data")
from nltk.metrics.distance import jaccard_distance
from nltk.util import ngrams

from nltk.corpus import words
from rake_nltk import Rake
from krovetzstemmer import Stemmer

nltk.data.path.append("/tmp/nltk_data")

correct_words = words.words()
rake_nltk_var = Rake()

ALPHABET = string.ascii_lowercase
STEMMER = Stemmer()

SEARCH_CUTOFF = 10

r = None
loop = asyncio.get_event_loop()

load_dotenv("..")

# app instance
app = Flask(__name__)
CORS(app)

def zero_list():
    return [0, 0]

async def retrieve_word_info(word):
    word = STEMMER.stem(word)
    word_dict = dict()
    urls = await r.smembers(f"word:{word}") # Get urls for word
    urls = list(urls)
    tasks = []
    n = 500
    for i in range(math.ceil(len(urls) / n)):
        sub = urls[i * n:(i + 1) * n]
        pipe = r.pipeline(transaction=False)
        for i in range(len(sub)):
            pipe.lrange(f"metadata:{word}:{urls[i].decode('utf-8')}", 0, -1)
        tasks.append(pipe.execute())
    start = time.time()
    raw = await asyncio.gather(*tasks)
    metadata_list = functools.reduce(lambda x, y: x+y, raw)
    print(f"It took {time.time() - start} seconds to run pipe function in retrieve_word_info for word: {word} for {len(urls)} commands")
    for i in range(len(urls)):
        metadata_list[i][0] = int(metadata_list[i][0].decode('utf-8')) 
        metadata_list[i][1] = float(metadata_list[i][1].decode('utf-8'))
        word_dict[urls[i]] = metadata_list[i]
    return word_dict

async def init_words_info(args):
    words_info = dict()
    tasks = []
    for word in args:
        tasks.append(retrieve_word_info(word))
    list_of_word_dicts = await asyncio.gather(*tasks)
    for i in range(len(args)):
        words_info[args[i]] = list_of_word_dicts[i]
    return words_info

async def add_titles(relevant_urls):
    tasks = []
    n = 500
    for i in range(len(relevant_urls)):
        relevant_urls[i] = relevant_urls[i].decode('utf-8')
    for i in range(math.ceil(len(relevant_urls) / n)):
        sub = relevant_urls[i * n:(i + 1) * n]
        pipe = r.pipeline(transaction=False)
        for i in range(len(sub)):
            pipe.get(f"title:{relevant_urls[i]}")
        tasks.append(pipe.execute())
    start = time.time()
    titles = functools.reduce(lambda x, y: x+y, await asyncio.gather(*tasks))
    print(f"TOOK THIS LONG TO GET TITLES: {time.time() - start}")
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


async def remove_least_relevant_words_info(words_info):
    avg_tfidfs = dict()
    for word, data in words_info.items():
        tfidfs = [tfidf for _, tfidf in data.values()]
        if len(tfidfs) > 0:
            avg_tfidfs[word] = sum(tfidfs) / len(tfidfs)

    least_relevant_word = get_least_relevant_word(avg_tfidfs)
    args = list(words_info.keys())
    args.remove(least_relevant_word)

    return await init_words_info(args)


async def autocorrect_words_info(words_info):
    keys = list(words_info.keys())
    args = list()

    for word in keys:
        temp = [
            (jaccard_distance(set(ngrams(word, 2)), set(ngrams(w, 2))), w)
            for w in correct_words
            if w[0] == word[0]
        ]
        args.append(sorted(temp, key=lambda val: val[0])[0][1])

    return await init_words_info(args)


async def get_keywords_words_info(words_info):
    keys = " ".join(list(words_info.keys()))

    rake_nltk_var.extract_keywords_from_text(keys)
    keyword_extracted = rake_nltk_var.get_ranked_phrases()
    args = [word for keyword in keyword_extracted for word in keyword.split()]
    
    return await init_words_info(args)


async def sort_relevant(words_info):  # sort relevance of url by highest tfidf score
    # FIRST screen
    print("1st screen: " + str(list(words_info.keys())))
    url_scores_list = calc_url_scores(and_query(words_info), words_info)

    # SECOND screen - extract keywords
    if len(url_scores_list) < SEARCH_CUTOFF:
        prev = len(url_scores_list)
        words_info = await get_keywords_words_info(words_info)
        print("2nd screen: " + str(list(words_info.keys())))
        new_urls = calc_new_url_scores(url_scores_list, words_info)
        if len(new_urls) > prev:
            url_scores_list = new_urls

    # THIRD screen - autocorrect words
    if len(url_scores_list) < SEARCH_CUTOFF:
        prev = len(url_scores_list)
        words_info = await autocorrect_words_info(words_info)
        print("3rd screen: " + str(list(words_info.keys())))
        new_urls = calc_new_url_scores(url_scores_list, words_info)
        if len(new_urls) > prev:
            url_scores_list = new_urls

    # FOURTH screen - remove least relevant tfidf score (often misinterpreted autocorrect)
    if len(url_scores_list) < SEARCH_CUTOFF and len(words_info) > 1:
        prev = len(url_scores_list)
        words_info = await remove_least_relevant_words_info(words_info)
        print("4th screen: " + str(list(words_info.keys())))
        new_urls = calc_new_url_scores(url_scores_list, words_info)
        if len(new_urls) > prev:
            url_scores_list = new_urls

    return url_scores_list

async def search(args):
    for i in range(len(args)):  # lowercase all words
        args[i] = args[i].lower()

    global r
    r = redis.Redis.from_url(os.environ["REDIS_URL"])

    # FIRST SCREEN - remove single characters
    args = list(filter(lambda x: len(x) > 1, args))
    start = time.time()
    words_info = await init_words_info(args)
    print(f"It took {time.time() - start} seconds to run init_words_info function in search")

    start = time.time()
    relevant_urls = await sort_relevant(words_info)
    print(f"It took {time.time() - start} seconds to run sort_relevant function in search")
    start = time.time()
    await add_titles(relevant_urls)
    print(f"It took {time.time() - start} seconds to run add_titles function in search")

    for i, url in enumerate(relevant_urls[:SEARCH_CUTOFF]):
        print(f"{i + 1}: {url[0]}, {url[1]}")
    print(len(relevant_urls))
    return relevant_urls

@app.route("/api/search", methods=["GET"])
def return_home():
    query = request.args.getlist("query")
    query_params = query[0].split(" ")
    length = int(request.args.getlist("length")[0])
    start = time.time()
    result = loop.run_until_complete(search(query_params))
    print(f"It took {time.time() - start} seconds to run search function")
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
    # res = asyncio.run(redis_get("test"))
    # print(res)
    # print(res.read())
    # print(res.url)
    # urls = loop.run_until_complete(add_titles(set()))