from dotenv import load_dotenv
import redis.asyncio as redis
import asyncio
import os
import json

# Convert inverted index and store on redis db hosted on local machine

async def main():

  INDEX_PATH="inverted_index/"

  load_dotenv()

  r = redis.Redis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"], password=os.environ["REDIS_PASS"], decode_responses=True)

  r.ping()
  print("connected to redis")

  counter = 0
  num_keys = 0
  pipe = r.pipeline()
  tasks = []
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
            pipe.setnx(f"title:{url}", title)
            pipe.sadd(f"word:{word}", url)
            _, _, important, tfidf = two_dict[word][key]
            pipe.rpush(f"metadata:{word}:{url}", important, tfidf)
            num_keys += 1
            if num_keys % 1000 == 999:
              tasks.append(pipe.execute())
              pipe = r.pipeline()
              if len(tasks) >= 10:
                await asyncio.gather(*tasks)
                tasks = []
  tasks.append(pipe.execute())
  await asyncio.gather(*tasks)

if __name__ == "__main__":
  asyncio.run(main())