from MediaGeneration.generate_media_files import generate_and_save_media_files
from VideoGeneration.video_generator import generate_youtube_video

if __name__ == "__main__":
    generate_and_save_media_files("askreddit")
    generate_youtube_video()
