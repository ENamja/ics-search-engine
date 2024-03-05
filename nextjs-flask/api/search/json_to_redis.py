from redis import Redis
from dotenv import load_dotenv
import os
import json

INDEX_PATH="inverted_index/"

load_dotenv()

r = Redis(
  host=os.environ['REDIS_HOST'],
  port=os.environ['REDIS_PORT'],
  password=os.environ['REDIS_PASS'])

r.ping()
print("connected to redis")

for filename in os.listdir(INDEX_PATH):
  with open(f"{INDEX_PATH}{filename}") as file:
    two_dict = json.load(file)
    for word in two_dict.keys():
      word_dict = two_dict[word]
      for url in word_dict.keys():
        count, total, important, tfidf = word_dict[url]
        r.rpush(f"{word}:{url}", count, total, important, tfidf)
