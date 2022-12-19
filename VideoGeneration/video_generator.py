from dataclasses import dataclass
from datetime import date
from random import choice
from typing import List
from moviepy.editor import *
from moviepy.video.fx.all import crop
from moviepy.audio.fx.all import audio_fadein, audio_fadeout
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


def split_video_clips_into_mp3_sized_chunks(image_audio_pair: List[ImageAudioPair], full_clip: VideoFileClip) -> list[CompositeVideoClip]:
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
        Logger.info(f"Appending {index + 1}/{len(image_audio_pair)} clips...")
        audio_clip_length = get_audio_file_duration(pair.audio)
        audio_clip = AudioFileClip(pair.audio)

        split_video_clip = full_clip.subclip(total_length, total_length + audio_clip_length)
        split_video_clip.audio = audio_clip

        image_clip = ImageClip(pair.image).set_position('center').set_duration(audio_clip_length)
        video_clips.append(CompositeVideoClip([split_video_clip, image_clip]))

        total_length += audio_clip_length

        written_index_value = str(index + 1) + {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <= index + 1 % 100 < 20 else index + 1 % 10, "th")
        Logger.info(f"Successfully appended {written_index_value} file.")

    return video_clips


def generate_youtube_video():
    """
    Creates a youtube video from the generated files.
    """
    Logger.info(f"Entering {generate_youtube_video.__name__}")

    clip: VideoFileClip = VideoFileClip(f"{MEDIA_URL}\\Videos\\video.mp4", audio=False)

    Logger.info(f"Resizing the main clip...")

    (w, h) = clip.size
    cropped_clip = crop(clip, width=600, height=720, x_center=w/2, y_center=h/2)
    resized_clip = cropped_clip.resize((1080, 1920)).subclip(15)

    Logger.info(f"Clip successfully resized.")

    image_audio_pairs: List[ImageAudioPair] = [
        ImageAudioPair(image=f"{MEDIA_URL}\\Images\\title.png",
                       audio=f"{MEDIA_URL}\\MP3s\\title.wav")
    ]

    image_audio_pairs.extend([ImageAudioPair(image=f"{MEDIA_URL}\\Images\\{x}.png", audio=f"{MEDIA_URL}\\MP3s\\{x}.wav") for x in range(0, 2)])

    video_clip_list = split_video_clips_into_mp3_sized_chunks(image_audio_pairs, resized_clip)

    Logger.info(f"Attempting to concatenate videos...")

    final_cut = concatenate_videoclips(video_clip_list)


    song_choice = choice(get_all_music_files())
    Logger.info(f"Attempting to add background music with song: {song_choice}")

    start_delay = 15
    background_audio = AudioFileClip(song_choice).subclip(start_delay, int(final_cut.duration + start_delay))
    background_audio = background_audio.fx(afx.volumex, 0.1)
    background_audio = audio_fadein(background_audio, 2)
    background_audio = audio_fadeout(background_audio, 2)
    final_audio = CompositeAudioClip([final_cut.audio, background_audio])
    final_cut.audio = final_audio

    Logger.info("Saving file.")

    final_cut.write_videofile(f"{ROOT_DIR}\\OutputFiles\\GeneratedVideos\\{date.today()}.mp4", codec='libx264')

def get_all_music_files() -> list[str]:
    """
    Gets all music files in the background music folder.
    :return: All music files in the background music folder.
    """
    # list to store files
    songs = []

    dir_path = f"{MEDIA_URL}\\BackgroundMusic\\"

    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            songs.append(path)

    return songs