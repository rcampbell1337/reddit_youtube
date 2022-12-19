from dataclasses import dataclass
from datetime import date
from typing import List
from moviepy.editor import *
from MediaGeneration.TTS.pyttsx3 import get_audio_file_duration
from definitions import MEDIA_URL, ROOT_DIR
from logger import Logger


@dataclass
class ImageAudioPair:
    """
    Dataclass representing an Image Audio Pair (For moviepy).
    """
    image: str
    audio: str


def split_video_clips_into_mp3_sized_chunks(image_audio_pair: List[ImageAudioPair], full_clip: VideoFileClip):
    """
    Splits all of the generated video clips into the size of the given MP3 Files.
    :param image_audio_pair: A given video clip.
    :param full_clip: The background video clip.
    :return: All of the video clips.
    """
    Logger.info(f"Entering {split_video_clips_into_mp3_sized_chunks.__name__}")

    total_length: int = 0
    video_clips = []
    for index, pair in enumerate(image_audio_pair):
        Logger.info(f"Appending {index}/{len(image_audio_pair)} clips...")
        audio_clip_length = get_audio_file_duration(pair.audio)
        audio_clip = AudioFileClip(pair.audio)

        split_video_clip = full_clip.subclip(total_length, total_length + audio_clip_length)
        split_video_clip.audio = audio_clip

        image_clip = ImageClip(pair.image).set_position('center').set_duration(audio_clip_length)
        video_clips.append(CompositeVideoClip([split_video_clip, image_clip]))

        total_length += audio_clip_length

        written_index_value = {str(index) + {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <= index % 100 < 20 else index % 10, "th")}
        Logger.info(f"Successfully appended {written_index_value} file.")

    return video_clips


def generate_youtube_video():
    """
    Creates a youtube video from the generated files.
    """
    Logger.info(f"Entering {generate_youtube_video.__name__}")

    clip = VideoFileClip(f"{MEDIA_URL}\\Videos\\video.mp4", audio=False)
    clip = clip.resize((1080, 1920))

    image_audio_pairs = [
        ImageAudioPair(image=f"{MEDIA_URL}\\Images\\title.png",
                       audio=f"{MEDIA_URL}\\MP3s\\title.wav"),
        ImageAudioPair(image=f"{MEDIA_URL}\\Images\\0.png",
                       audio=f"{MEDIA_URL}\\MP3s\\0.wav"),
        ImageAudioPair(image=f"{MEDIA_URL}\\Images\\1.png",
                       audio=f"{MEDIA_URL}\\MP3s\\1.wav"),
        ImageAudioPair(image=f"{MEDIA_URL}\\Images\\2.png",
                       audio=f"{MEDIA_URL}\\MP3s\\2.wav"),
    ]


    video_clip_list = split_video_clips_into_mp3_sized_chunks(image_audio_pairs, clip)

    Logger.info(f"Attempting to concatenate videos...")

    concatenate_videoclips(video_clip_list)\
        .write_videofile(f"{ROOT_DIR}\\VideoGeneration\\output_video\\{date.today()}.mp4", codec='libx264')