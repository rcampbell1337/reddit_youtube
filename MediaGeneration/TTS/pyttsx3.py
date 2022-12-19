import os
import pyttsx3
from typing import List
from pyttsx3 import Engine
from definitions import MEDIA_URL
from pydub import AudioSegment
from logger import Logger


def pyttsx3_text_to_speech(things_to_say: List[str]) -> None:
    """
    Converts text content into an MP3 TTS file.
    :param things_to_say: A list of things to be converted to MP3 format.
    """
    Logger.info(f"Entering {pyttsx3_text_to_speech.__name__}")

    converter = pyttsx3.init()
    converter.setProperty('rate', 175)
    converter.setProperty('volume', 0.7)
    converter.setProperty('voice',
                          'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')

    Logger.info("Attempting to convert files to mp3...")

    if len(things_to_say) > 1:
        [format_audio_file(converter, thing_to_say, f"{MEDIA_URL}\\MP3s\\{index}.wav")
            for index, thing_to_say
            in enumerate(things_to_say)]

    else:
        format_audio_file(converter, things_to_say[0], os.path.abspath(f"{MEDIA_URL}\\MP3s\\title.wav"))

    Logger.info("Successfully converted files to mp3.")

def trial_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print(voice, voice.id)
        engine.setProperty('voice', voice.id)
        engine.say("Hello World!")
        engine.runAndWait()
        engine.stop()



def format_audio_file(converter: Engine, text_content: str, path: str) -> None:
    """
    Formats an audio file into a MP3 File.
    :param converter: The converter engine.
    :param text_content: The text content to be converted.
    :param path: The path to save the file to.
    """
    Logger.info(f"Entering {format_audio_file.__name__}")

    converter.save_to_file(text_content, path)
    converter.runAndWait()


def get_audio_file_duration(path: str, retries = 0) -> int:
    """
    Gets the duration of a given audio file.
    :param path: The path to the audio file.
    :param retries: The number of times this has been attempted.
    :return: The length of the audio file.
    """
    Logger.info(f"Entering {get_audio_file_duration.__name__}")

    try:
        return AudioSegment.from_wav(path).duration_seconds
    except FileNotFoundError:
        if retries > 5:
            raise FileNotFoundError("Could not find the file specified.")

        Logger.warning(f"Could not find file, trying again with path {path}...")
        get_audio_file_duration(path, retries + 1)
