from pytube import YouTube
from MediaGeneration.Youtube.youtube_api import get_first_yt_video


def store_youtube_video(relative_path: str) -> None:
    yt = YouTube(get_first_yt_video())
    youtube_video = yt.streams.filter(progressive=True, file_extension='mp4')\
                      .order_by('resolution')\
                      .desc()\
                      .first()

    gigabyte: int = 1073741824

    if youtube_video.filesize_approx > gigabyte:
        print("File was too big for storage.")
        return store_youtube_video(relative_path=relative_path)

    youtube_video.download(output_path=f"{relative_path}/Videos", filename="video.mp4")