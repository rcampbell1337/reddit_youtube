from dataclasses import dataclass
from typing import List
from MediaGeneration.Reddit.reddit_image_handler import store_post_images
from decouple import config
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

    @staticmethod
    def connect_to_reddit_api() -> praw.Reddit:
        """
        Connects to the Reddit API and returns an instance of a Reddit API Connection.
        :return: An instance of a Reddit API Connection
        """
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
        """
        Gets all of the information for a given Reddit post.
        :return: All of the information for a given Reddit post
        """
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

        return post

    def store_images_of_title_and_top_three_comments(self) -> None:
        """
        Stores the images of the top three Reddit Comments.
        :return: None.
        """
        store_post_images(self.get_reddit_page_url(self.post_info))

    def get_reddit_page_url(self, post: Post) -> str:
        """
        Constructs a link to a given post on a subreddit.
        :param post: The post.
        :return: A link to a given post on a subreddit.
        """
        return f"https://www.reddit.com/r/{self.subreddit}/comments/{post.id}"

