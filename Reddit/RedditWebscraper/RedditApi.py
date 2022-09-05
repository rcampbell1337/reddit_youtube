from dataclasses import dataclass
from typing import List
from decouple import config
from Reddit.Api import Api
import praw


@dataclass
class Comment:
    author: str
    body: str
    score: int


@dataclass
class Post:
    subreddit: str
    author: str
    num_comments: int
    title: str
    comments: List[Comment]


class RedditApi(Api):
    def __init__(self):
        self.reddit_instance = self.connect_to_reddit_api()

    def get_list_of_posts(self) -> List[str]:
        return ["Hello", "Joe"]

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

    def get_post_information(self, subreddit: str):
        submission = next(self.reddit_instance.subreddit(subreddit).top(time_filter="week"))
        comments = list(map(lambda comment: Comment(comment.author, comment.body, comment.score),
                        submission.comments[:3]))
        post = Post(subreddit, submission.author, submission.num_comments, submission.title, comments)
        return post

