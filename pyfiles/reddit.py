import praw
import random

reddit = praw.Reddit(client_id="Client ID",
                     client_secret="Client Secret",
                     user_agent="User Agent")

print(f"Logged in as {reddit.user.me()}")


def meme(subreddit):
    subreddit = reddit.subreddit(f"{subreddit}")
    memes = []
    for submission in subreddit.hot(limit=50):
        if not submission.stickied:
            memes.append(submission)

    choice = random.choice(range(len(memes)))

    title = memes[choice].title
    url = memes[choice].url

    result = {
        'title': title,
        'url': url,
    }
    return result
