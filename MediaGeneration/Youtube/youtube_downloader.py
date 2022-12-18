from pytube import YouTube
from MediaGeneration.Youtube.youtube_api import get_random_yt_video
from definitions import MEDIA_URL


def store_youtube_video() -> None:
    """
    Saves a given Youtube video.
    """
    yt = YouTube(get_first_yt_video())
    youtube_video = yt.streams.filter(progressive=True, file_extension='mp4')\
                      .order_by('resolution')\
                      .desc()\
                      .first()

    gigabyte: int = 1073741824

    if youtube_video.filesize_approx > gigabyte:
        print("File was too big for storage.")
        return store_youtube_video()

    youtube_video.download(output_path=f"{MEDIA_URL}/Videos", filename="video.mp4")