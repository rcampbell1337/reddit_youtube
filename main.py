from Reddit.reddit_api import RedditApi
from TTS.pyttsx3 import pyttsx3_text_to_speech
from Youtube.youtube_downloader import store_youtube_video

if __name__ == "__main__":
    ask_reddit_link = RedditApi("askreddit")
    ask_reddit_link.store_images_of_title_and_top_three_comments()
    store_youtube_video()
    pyttsx3_text_to_speech(ask_reddit_link.post_info.title)
    pyttsx3_text_to_speech([comment.body for comment in ask_reddit_link.post_info.comments])
