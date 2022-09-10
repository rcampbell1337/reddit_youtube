from dataclasses import dataclass
from typing import List
from Reddit.reddit_image_handler import store_web_image
from decouple import config
import praw


@dataclass
class Comment:
    author: str
    body: str
    score: int


@dataclass
class Post:
    id: str
    subreddit: str
    author: str
    num_comments: int
    title: str
    comments: List[Comment]


class RedditApi:
    def __init__(self, subreddit: str):
        self.reddit_instance = self.connect_to_reddit_api()
        self.subreddit = subreddit

    @staticmethod
    def connect_to_reddit_api() -> praw.Reddit:
        username: str = config("USER")
        password: str = config("PASSWORD")
        client: str = config("REDDIT_CLIENT")
        secret: str = config("REDDIT_SECRET")

        reddit = praw.Reddit(
            client_id=client,
            client_secret=secret,
            password=password,
            user_agent="yt-generator",
            username=username,
        )

        return reddit

    def get_post_information(self) -> Post:
        submission = next(self.reddit_instance.subreddit(self.subreddit).top(time_filter="week"))
        comments = [Comment(comment.author, comment.body, comment.score) for comment in submission.comments[:3]]
        post = Post(submission, self.subreddit, submission.author, submission.num_comments, submission.title, comments)
        return post

    def store_images_of_title_and_top_three_comments(self) -> None:
        store_web_image(self.get_reddit_page_url(self.get_post_information()))

    def get_reddit_page_url(self, post: Post) -> str:
        return f"https://www.reddit.com/r/{self.subreddit}/comments/{post.id}"
