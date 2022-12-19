from dataclasses import dataclass
from typing import List
from MediaGeneration.Reddit.reddit_image_handler import store_post_images
from decouple import config
from logger import Logger
import praw


@dataclass
class Comment:
    """
    Dataclass Representing a comment on Reddit.
    """
    author: str
    body: str
    score: int


@dataclass
class Post:
    """
    Dataclass representing a Post on reddit.
    """
    subreddit: str
    id: str
    author: str
    num_comments: int
    title: str
    comments: List[Comment]


class RedditApi:
    """
    Class that handles interacting with the Reddit API.
    """
    def __init__(self, subreddit: str):
        self.subreddit = subreddit
        self.reddit_instance = self.connect_to_reddit_api()
        self.post_info = self.get_post_information()

    def connect_to_reddit_api(self) -> praw.Reddit:
        """
        Connects to the Reddit API and returns an instance of a Reddit API Connection.
        :return: An instance of a Reddit API Connection.
        """
        Logger.info(f"Entering {self.connect_to_reddit_api.__name__}")

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

        Logger.info(f"Successfully created an instance of the Reddit API.")

        return reddit

    def get_post_information(self) -> Post:
        """
        Gets all of the information for a given Reddit post.
        :return: All of the information for a given Reddit post
        """
        Logger.info(f"Entering {self.get_post_information.__name__}")

        submission = next(self.reddit_instance.subreddit(self.subreddit).top(time_filter="week"))
        comments = [Comment(author=comment.author,
                            body=comment.body,
                            score=comment.score) for comment in submission.comments[:3]]

        post = Post(subreddit=self.subreddit,
                    id=submission,
                    author=submission.author,
                    num_comments=submission.num_comments,
                    title=submission.title,
                    comments=comments)

        Logger.info(f"Successfully retrieved title and comments of Reddit Post.")

        return post

    def store_images_of_title_and_top_three_comments(self) -> None:
        """
        Stores the images of the top three Reddit Comments.
        """
        store_post_images(f"https://www.reddit.com/r/{self.subreddit}/comments/{self.post_info.id}")

