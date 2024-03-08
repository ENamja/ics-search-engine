from dotenv import load_dotenv
import redis
import os
import json

# Convert inverted index and store on redis db hosted on local machine

def main():

  INDEX_PATH="inverted_index/"

  load_dotenv()

  r = redis.Redis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"], decode_responses=True)

  r.ping()
  print("connected to redis")

  counter = 0
  for filename in os.listdir(INDEX_PATH):
    with open(f"{INDEX_PATH}{filename}") as file:
      print(f"file: {filename}, counter: {counter}")
      counter += 1
      two_dict = json.load(file)
      for word in two_dict.keys():
        keys = two_dict[word].keys()
        if len(keys):
          for key in keys:
            url, title = key.split(" <%split%> ", 1)
            r.setnx(f"title:{url}", title)
            r.sadd(f"word:{word}", url)
            _, _, important, tfidf = two_dict[word][key]
            r.rpush(f"metadata:{word}:{url}", important, tfidf)

if __name__ == "__main__":
  main()