import praw
import json
from praw.models import MoreComments
import time

reddit = praw.Reddit(
    client_id="WsogRN4I_9qpHjYFx040Yg",
    client_secret="IvpOWdceYYS07YyjnxtnVEoF2spNCw",
    user_agent="my user agent",
)

def scrape_posts(subreddit_name, num_posts, output_file):
    # Load existing data from the output file, if it exists
    try:
        with open(output_file, 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    subreddit = reddit.subreddit(subreddit_name)
    top_posts = subreddit.top(limit=num_posts)  # Fetch top posts from subreddit
    new_posts = subreddit.new(limit=100)  # New posts

    processed_ids = set()  # Initialize a set to store processed post IDs. Using this to handle duplicates

    # THIS LOOP IS FOR TOP POSTS
    for post in top_posts:  # Looking at each top post
        if post.id not in processed_ids:
            # Using dictionary to store data easier
            post_data = {
                'title': post.title,
                'author': post.author.name if post.author else '[deleted]',
                'score': post.score,
                'created_utc': post.created_utc,
                'num_comments': post.num_comments,
                'permalink': post.permalink,
                'url': post.url,
                'top_comments': []  # Initialize list to store top comments
            }

            # Fetch top comments for the post
            submission = reddit.submission(id=post.id)  # Takes the posts individual id to take a look at comments
            submission.comments.replace_more(limit=0)  # handles AttributeError: 'MoreComments' object it replaces or removes MoreComments objects from the forest.
            comment_count = 0
            for comment in submission.comments:
                if comment.score > 100:  # Filter comments by score, adjust threshold as needed
                    post_data['top_comments'].append({'body': comment.body, 'score': comment.score})
                    comment_count += 1
                    if comment_count >= 50:  # Take 50 comments if upvote score > 100
                        break

            existing_data.append(post_data)
            processed_ids.add(post.id)

    # THIS LOOPS HANDLES NEW POSTS
    for post in new_posts:  # Looking at each new post
        if post.id not in processed_ids:
            # Using dictionary to store data easier
            post_data = {
                'title': post.title,
                'author': post.author.name if post.author else '[deleted]',
                'score': post.score,
                'created_utc': post.created_utc,
                'num_comments': post.num_comments,
                'permalink': post.permalink,
                'url': post.url,
                'top_comments': []  # Initialize list to store top comments
            }

            # Fetch top comments for the post
            submission = reddit.submission(id=post.id)  # Takes the posts individual id to take a look at comments
            submission.comments.replace_more(limit=0)  # handles AttributeError: 'MoreComments' object it replaces or removes MoreComments objects from the forest.
            comment_count = 0
            for comment in submission.comments:
                if comment.score > 20:  # Filter comments by score, adjust threshold as needed lowering the score for new posts
                    post_data['top_comments'].append({'body': comment.body, 'score': comment.score})
                    comment_count += 1
                    if comment_count >= 50:  # Take 50 comments if upvote score > 20
                        break

            existing_data.append(post_data)
            processed_ids.add(post.id)

    # Write data to JSON file
    with open(output_file, 'w') as file:
        json.dump(existing_data, file, indent=4)

subreddit_name = 'aww'  # subreddit u want to crawl
num_posts = 1000  # No of posts you want to crawl
output_file = 'reddit_posts.json'

retry_delay = 10 # Initial delay in seconds
max_retries = 10  # Maximum number of retries

for attempt in range(max_retries):
    try:
        scrape_posts(subreddit_name, num_posts, output_file)
        break  # Break out of the loop if successful
    except praw.exceptions.APIException as e:
        if e.error_type == 'RATELIMIT':
            print(f"Rate limit exceeded. Retrying in {retry_delay} seconds.")
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff
        else:
            raise  # Re-raise other API exceptions
else:
    raise Exception("Max retries exceeded. Unable to scrape posts.")