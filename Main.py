from Reddit.RedditWebscraper.RedditApi import RedditApi
from TTS.pyttsx3 import pyttsx3_text_to_speech

if __name__ == "__main__":
    comments = RedditApi().get_post_information("askreddit").comments
    pyttsx3_text_to_speech([comment.body for comment in comments])
