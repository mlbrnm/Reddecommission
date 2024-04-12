import json
import random
import time
import praw
from openai import OpenAI

# Load the configuration from the JSON file
with open("config.json") as f:
    config = json.load(f)

client = OpenAI(api_key=config["openai_key"])

reddit = praw.Reddit(
    client_id=config["client_id"],
    client_secret=config["client_secret"],
    user_agent=config["user_agent"],
    username=config["username"],
    password=config["password"]
)

def main():
  print("-"*50)
  print(f"Signed into Reddit account '{config['username']}'")

  while True:
    print(f"Choosing from the following subreddits:")
    print(config["possible_subreddits"])
    subreddit = reddit.subreddit(random.choice(config["possible_subreddits"]))
    print(f"Subreddit: {subreddit.display_name}")
    possible_posts = []

    for submission in subreddit.new():
        if submission.is_self:
            possible_posts.append(submission)

    post_to_reply = random.choice(possible_posts)
    post_title = post_to_reply.title
    post_body = post_to_reply.selftext

    print(f"\nPOST TITLE:\n{post_title}")
    print(f"\nPOST CONTENT:\n{post_body}")

    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": f"{config['primary_prompt']}\n{config['secondary_prompt']}"},
        {"role": "user", "content": f"{post_title}\n{post_body}"}
      ]
    )

    reply = completion.choices[0].message.content
    print(f"\nREPLY:\n{reply}\n")

    post_to_reply.reply(reply)

    next_run_delay = random.randint(120,1800)
    print(f"The program will continue to run until aborted. Press Ctrl-C to abort, or close the Python terminal. Next run in {next_run_delay/60:.1f} minutes.\n")
    time.sleep(next_run_delay)

if __name__ == "__main__":
    main()
