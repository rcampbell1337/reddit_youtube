from Reddit.reddit_api import RedditApi
from TTS.pyttsx3 import pyttsx3_text_to_speech

if __name__ == "__main__":
    comments = RedditApi("askreddit").get_post_information().comments
    pyttsx3_text_to_speech([comment.body for comment in comments])
