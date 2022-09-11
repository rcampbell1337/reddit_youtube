from dataclasses import dataclass
from typing import List
from MediaGeneration.Reddit.reddit_image_handler import store_web_image
from decouple import config
import praw


@dataclass
class Comment:
    author: str
    body: str
    score: int


@dataclass
class Post:
    subreddit: str
    id: str
    author: str
    num_comments: int
    title: str
    comments: List[Comment]


class RedditApi:
    def __init__(self, subreddit: str, relative_path: str):
        self.reddit_instance = self.connect_to_reddit_api()
        self.relative_path = relative_path
        self.subreddit = subreddit
        self.post_info = self.get_post_information()

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
        submission = next(self.reddit_instance.subreddit(self.subreddit).top(time_filter="day"))
        comments = [Comment(author=comment.author,
                            body=comment.body,
                            score=comment.score) for comment in submission.comments[:3]]

        post = Post(subreddit=self.subreddit,
                    id=submission,
                    author=submission.author,
                    num_comments=submission.num_comments,
                    title=submission.title,
                    comments=comments)

        return post

    def store_images_of_title_and_top_three_comments(self) -> None:
        store_web_image(self.get_reddit_page_url(self.post_info), self.relative_path)

    def get_reddit_page_url(self, post: Post) -> str:
        return f"https://www.reddit.com/r/{self.subreddit}/comments/{post.id}"

