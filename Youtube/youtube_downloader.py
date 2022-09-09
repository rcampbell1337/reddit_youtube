from pytube import YouTube
from Youtube.youtube_api import get_first_yt_video

yt = YouTube(get_first_yt_video())
yt.streams.filter(progressive=True, file_extension='mp4')\
    .order_by('resolution')\
    .desc()\
    .first()\
    .download(output_path="youtube_videos")
