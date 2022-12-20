from MediaGeneration.generate_media_files import generate_and_save_media_files
from VideoGeneration.video_generator import generate_youtube_video
from MediaGeneration.Youtube.youtube_api import upload_video_to_youtube
from MediaGeneration.Reddit.reddit_api import Post

if __name__ == "__main__":
    post_data: Post = generate_and_save_media_files("askreddit")
    video_file = generate_youtube_video()
    tags = ["askreddit", "reddit", "smash", "interesting"]
    tags.extend([word for word in post_data.title.split()])
    upload_video_to_youtube(video_file, post_data.title, tags)
